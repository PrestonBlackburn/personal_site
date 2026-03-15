// ── Configuration ────────────────────────────────────────────
const CAPTURE_INTERVAL = 10;

// ── State ───────────────────────────────────────────────────
let modelsLoaded = false;
let capturing = false;
let countdown = CAPTURE_INTERVAL;
let countdownTimer = null;

// ── DOM refs ───────────────────────────────────────────────
const video        = document.getElementById("webcam");
const overlay      = document.getElementById("overlay");
const timerEl      = document.getElementById("timer");
const statusEl     = document.getElementById("statusText");
const resultEl     = document.getElementById("latestResult");
const shopListEl  = document.getElementById("shoppersList");
const unmatchedEl  = document.getElementById("unmatchedFaces");
const unmatchedCnt = document.getElementById("unmatchedCount");
const passwordEl   = document.getElementById("apiPassword");

// ── Helpers ─────────────────────────────────────────────────

function setStatus(msg, isError) {
  statusEl.textContent = msg;
  statusEl.style.color = isError ? "#dc2626" : "#666";
}

/**
 * Convert the current video frame to a JPEG Blob via an off-screen canvas.
 */
function captureFrameBlob() {
  const canvas = document.createElement("canvas");
  canvas.width  = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  return new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.85));
}

// ── Face-api.js initialisation ──────────────────────────────

async function loadModels() {
  const MODEL_URL = "https://justadudewhohacks.github.io/face-api.js/models";
  setStatus("Loading face-detection models...");
  try {
    await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
    modelsLoaded = true;
    setStatus("Models loaded. Starting webcam...");
  } catch (err) {
    setStatus("Failed to load face-detection models: " + err.message, true);
    console.error(err);
  }
}

// ── Webcam ──────────────────────────────────────────────────

async function startWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } },
    });
    video.srcObject = stream;
    await video.play();

    // Match overlay canvas size to video
    overlay.width  = video.videoWidth;
    overlay.height = video.videoHeight;

    setStatus("Webcam active. Detecting faces...");
    detectLoop();        // continuous face-box drawing
    startCaptureLoop();  // 10-second capture cycle
  } catch (err) {
    setStatus("Cannot access webcam: " + err.message, true);
    console.error(err);
  }
}

// ── Continuous face-detection overlay ───────────────────────

async function detectLoop() {
  if (!modelsLoaded) return;
  const ctx = overlay.getContext("2d");

  async function tick() {
    const detections = await faceapi.detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions()
    );

    ctx.clearRect(0, 0, overlay.width, overlay.height);

    // Scale boxes to match the actual video resolution
    const resized = faceapi.resizeResults(detections, {
      width: overlay.width,
      height: overlay.height,
    });

    resized.forEach((det) => {
      const { x, y, width, height } = det.box;
      ctx.strokeStyle = "#00e676";
      ctx.lineWidth   = 2;
      ctx.strokeRect(x, y, width, height);
    });

    requestAnimationFrame(tick);
  }

  tick();
}

// ── 10-second capture cycle ─────────────────────────────────

function startCaptureLoop() {
  countdown = CAPTURE_INTERVAL;
  updateTimerDisplay();

  countdownTimer = setInterval(async () => {
    countdown--;
    updateTimerDisplay();

    if (countdown <= 0) {
      clearInterval(countdownTimer);
      await performCapture();
      // Restart the countdown after capture completes
      startCaptureLoop();
    }
  }, 1000);
}

function updateTimerDisplay() {
  timerEl.textContent = `Next capture in: ${countdown}s`;
}

async function performCapture() {
  if (capturing) return;
  capturing = true;
  setStatus("Capturing face...");

  try {
    const blob = await captureFrameBlob();

    const formData = new FormData();
    formData.append("file", blob, "capture.jpg");

    const headers = {};
    if (passwordEl.value) {
      headers["X-API-Password"] = passwordEl.value;
    }

    const res  = await fetch(`/face/compare-face`, { 
      method: "POST", 
      body: formData,
      headers 
    });
    const data = await res.json();

    if (res.status === 401) {
      showResult(`Error: Invalid password`, false);
      setStatus("Authentication failed", true);
    } else if (res.status === 429) {
      showResult(`Error: Rate limit exceeded`, false);
      setStatus("Rate limited - try again later", true);
    } else if (!res.ok) {
      showResult(`Error: ${data.detail || res.statusText}`, false);
      setStatus("Capture failed", true);
    } else if (data.match_found) {
      showResult(
        `Match: <strong>${data.shopper}</strong> (confidence ${(data.confidence * 100).toFixed(1)}%)`,
        true
      );
      setStatus("Match found!");
    } else {
      showResult(
        `No match (closest: ${data.closest_match || "N/A"}, similarity ${((data.closest_similarity || 0) * 100).toFixed(1)}%)`,
        false
      );
      setStatus("No match — face tracked as unmatched");
      fetchUnmatchedFaces();
    }
  } catch (err) {
    showResult("Network error — is the backend running?", false);
    setStatus("Backend unreachable", true);
    console.error(err);
  } finally {
    capturing = false;
  }
}

function showResult(html, isMatch) {
  resultEl.innerHTML = `<div class="p-3 rounded text-sm ${isMatch ? "bg-green-50 border-l-4 border-green-500" : "bg-orange-50 border-l-4 border-orange-500"}">${html}</div>`;
}

// ── Fetch helpers ───────────────────────────────────────────

async function fetchShoppers() {
  try {
    const res  = await fetch(`/face/shoppers`);
    const data = await res.json();
    const list = data.shoppers || [];
    if (list.length === 0) {
      shopListEl.innerHTML = '<span class="text-gray-400 italic text-sm">No celebrities indexed on backend</span>';
    } else {
      shopListEl.innerHTML = list.map((c) => `<span class="inline-block bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm m-1">${c}</span>`).join(" ");
    }
  } catch {
    shopListEl.innerHTML = '<span class="text-gray-400 italic text-sm">Could not reach backend</span>';
  }
}

async function fetchUnmatchedFaces() {
  try {
    const res  = await fetch(`/face/unmatched-faces`);
    const data = await res.json();
    const list = data.unmatched_faces || [];
    unmatchedCnt.textContent = list.length;
    if (list.length === 0) {
      unmatchedEl.innerHTML = '<span class="text-gray-400 italic text-sm">None yet</span>';
    } else {
      unmatchedEl.innerHTML = list
        .map(
          (f) =>
            `<div class="bg-pink-50 p-2 rounded text-sm my-1">ID: ${f.id.slice(0, 8)}... | ` +
            `Closest: ${f.closest_match || "N/A"} (${((f.closest_similarity || 0) * 100).toFixed(1)}%) | ` +
            `${new Date(f.timestamp).toLocaleTimeString()}</div>`
        )
        .join("");
    }
  } catch {
    unmatchedEl.innerHTML = '<span class="text-gray-400 italic text-sm">Could not reach backend</span>';
  }
}

// ── Bootstrap ───────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", async () => {
  await loadModels();
  await startWebcam();
  fetchShoppers();
  fetchUnmatchedFaces();
});
