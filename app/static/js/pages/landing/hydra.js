// ---------- HYDRA ----------
const hydraCanvas = document.getElementById("hydraCanvas");
// Make canvas fill the screen at device resolution
hydraCanvas.width = window.innerWidth * window.devicePixelRatio;
hydraCanvas.height = window.innerHeight * window.devicePixelRatio;
hydraCanvas.style.width = "100%";
hydraCanvas.style.height = "100%";

const hydra = new Hydra({ 
    canvas: hydraCanvas, 
    detectAudio: false, 
    width: hydraCanvas.width,
    height: hydraCanvas.height,
});


function hydraWave() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    //filet mignon
    // AFALFL
    // instagram/a_f_alfl 
    osc(100,-0.0018,0.17).diff(osc(20,0.00008).rotate(Math.PI/0.00003))
        .modulateScale(noise(1.5,0.18).modulateScale(osc(13).rotate(()=>Math.sin(time/22))),3)
        .color(11,0.5,0.4, 0.9, 0.2, 0.011, 5, 22,  0.5, -1).contrast(1.4)
        .add(src(o0).modulate(o0,.04),.6, .9)
        //.pixelate(0.4, 0.2, 0.1)
        .invert().brightness(0.0003, 2).contrast( 0.5, 2, 0.1, 2).color(4, -2, 0.1)
        .modulateScale(osc(2),-0.2, 2, 1, 0.3)
        .posterize(200) .rotate(1, 0.2, 0.01, 0.001)
        .color(22, -2, 0.5, 0.5, 0.0001,  0.1, 0.2, 8).contrast(0.18, 0.3, 0.1, 0.2, 0.03, 1) . brightness(0.0001, -1, 10)
            .out()
}

function hydraVoronoi() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    //tropical juice
    //by Ritchse
    //instagram.com/ritchse
    voronoi(2,0.3,0.2).shift(0.5)
    .modulatePixelate(voronoi(4,0.2),32,2)
    .scale(()=>1+(Math.sin(time*2.5)*0.05))
    .diff(voronoi(3).shift(0.6))
    .diff(osc(2,0.15,1.1).rotate())
    .brightness(0.1).contrast(1.2).saturate(1.2)
        .out()
}

function hydraOjack() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // by Olivia Jack
    // https://ojack.github.io

    osc(4, 0.1, 0.8).color(1.04,0, -1.1).rotate(0.30, 0.1).pixelate(2, 20).modulate(noise(2.5), () => 1.5 * Math.sin(0.08 * time)).out(o0)
}

function hydraOrbs() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    //CNDSD
    //http://malitzincortes.net/
    //ameba

    osc(15, 0.01, 0.1).mult(osc(1, -0.1).modulate(osc(2).rotate(4,1), 20))
    .color(0,2.4,5)
    .saturate(0.4)
    .luma(1,0.1, (6, ()=> 1 + a.fft[3]))
    .scale(0.7, ()=> 0.7 + a.fft[3])
    .diff(o0)// o0
    .out(o0)// o1
}

function hydraRetro() {
    // licensed with CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
    // by Zach Krall
    // http://zachkrall.online/

    osc(2, 0.9, 300)
    .color(0.9, 0.7, 0.8)
    .diff(
    osc(45, 0.3, 100)
    .color(0.9, 0.9, 0.9)
    .rotate(0.18)
    .pixelate(12)
    .kaleid()
    )
    .scrollX(10)
    .colorama()
    .luma()
    .repeatX(4)
    .repeatY(4)
    .modulate(
    osc(1, -0.9, 300)
    )
    .scale(2)

    .out()
}


const hydraFuncs = [hydraWave, hydraVoronoi, hydraOjack, hydraOrbs, hydraRetro];
const randomIndex = Math.floor(Math.random() * hydraFuncs.length);

// Get the random element
const randomHydra = hydraFuncs[randomIndex];
randomHydra();