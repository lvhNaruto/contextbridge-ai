"""Live upload verification through deployed Cloud Run stack (P0-9d)."""

import json
import time
from pathlib import Path
import urllib.request

API = "https://contextbridge-api-c5ltxo3mkq-uc.a.run.app"
SAMPLE_PATH = Path("uploaded_videos/an-702dbd15a78e/cb-sample.mp4")


def test_live_upload():
    assert SAMPLE_PATH.exists(), f"Sample video not found at {SAMPLE_PATH}"
    print(f"1. Preparing video: {SAMPLE_PATH} ({SAMPLE_PATH.stat().st_size / (1024*1024):.2f} MB)...")

    # Construct multipart/form-data
    boundary = "----WebKitFormBoundaryContextBridgeLive"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="video"; filename="cb-sample.mp4"\r\n')
    body.extend(b"Content-Type: video/mp4\r\n\r\n")
    body.extend(SAMPLE_PATH.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode())

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    }

    print("2. Uploading to POST /analyses on Cloud Run (synchronous Gemini analysis)...")
    start = time.time()
    req = urllib.request.Request(f"{API}/analyses", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        duration = time.time() - start
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        data = json.loads(resp.read().decode())
        analysis_id = data["id"]
        print(f"   -> Upload & analysis completed in {duration:.1f}s!")
        print(f"   -> Received analysis ID: {analysis_id}")

    print(f"3. Fetching full lesson from GET /analyses/{analysis_id}...")
    req = urllib.request.Request(f"{API}/analyses/{analysis_id}")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        lesson = json.loads(resp.read().decode())
        print(f"   -> Title: {lesson.get('title')}")
        print(f"   -> Duration: {lesson.get('durationSeconds')}s")
        print(f"   -> Chapters: {len(lesson.get('chapters', []))}")
        for ch in lesson.get("chapters", []):
            print(f"      * [{ch.get('startSeconds')}s - {ch.get('endSeconds')}s] {ch.get('title')} (confidence: {ch.get('confidence')})")
        print(f"   -> Transcript items: {len(lesson.get('transcript', []))}")
        print(f"   -> Contradictions: {len(lesson.get('contradictions', []))}")

    print(f"4. Asking a question to the newly analyzed video on Cloud Run...")
    q_data = json.dumps({"question": "What is covered in this video?"}).encode()
    req = urllib.request.Request(
        f"{API}/analyses/{analysis_id}/questions",
        data=q_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        ans = json.loads(resp.read().decode())
        print(f"   -> Answer: {ans.get('text')}")
        print(f"   -> Evidence: {ans.get('answer', {}).get('evidence')}")

    print("\nP0-9d LIVE UPLOAD VERIFICATION PASSED!")


if __name__ == "__main__":
    test_live_upload()
