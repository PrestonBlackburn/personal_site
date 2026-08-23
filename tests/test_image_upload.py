
import os
import sys
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
TOKEN = os.environ.get("IMAGE_API_TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}

# requests wants a list of (field_name, (filename, file_obj, content_type)) tuples
def test_image_upload(file_paths:list[str]):
    files = []
    open_handles = []
    for path in file_paths:
        if not os.path.isfile(path):
            print(f"ERROR: file not found: {path}")
            sys.exit(1)
        f = open(path, "rb")
        open_handles.append(f)
        files.append(("files", (os.path.basename(path), f, "application/octet-stream")))

    try:
        print(f"Uploading {len(files)} file(s) to {BASE_URL}/api/v1/images ...")
        response = requests.post(f"{BASE_URL}/api/v1/images", headers=headers, files=files)
    finally:
        for f in open_handles:
            f.close()
    print(response.text)
    assert response.status_code == 200, f"Upload failed: {response.status_code} {response.text}"

def test_list_images():
    list_resp = requests.get(f"{BASE_URL}/api/v1/images", headers=headers)
    assert list_resp.status_code == 200, f"List failed: {list_resp.status_code} {list_resp.text}"
    data = list_resp.json()
    filenames = [img["filename"] for img in data["images"]]
    assert "argocd.png" in filenames, f"Expected argocd.png in {filenames}"


def test_get_images(file_name: str):
    file_resp = requests.get(f"{BASE_URL}/api/v1/images/{file_name}", headers=headers)
    print(file_resp)
    assert file_resp.status_code == 200, f"Download failed: {file_resp.status_code} {file_resp.text}"

def test_delete_image(file_name: str):
    delete_resp = requests.delete(f"{BASE_URL}/api/v1/images/{file_name}", headers=headers)
    print(delete_resp.text)
    assert delete_resp.status_code == 200, f"Delete failed: {delete_resp.status_code} {delete_resp.text}"

    # confirm it's actually gone
    list_resp = requests.get(f"{BASE_URL}/api/v1/images", headers=headers)
    filenames = [img["filename"] for img in list_resp.json()["images"]]
    assert file_name not in filenames, f"{file_name} still present after delete: {filenames}"

if __name__ == "__main__":
    test_image_paths = ["./argocd.png"]
    test_image_upload(test_image_paths)
    test_list_images()
    test_get_images("argocd.png")
    test_delete_image("argocd.png")