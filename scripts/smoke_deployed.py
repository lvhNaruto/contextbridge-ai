"""End-to-end integration smoke test on deployed Cloud Run services (P0-9c)."""

import json
import urllib.error
import urllib.request

API = "https://contextbridge-api-c5ltxo3mkq-uc.a.run.app"
WEB = "https://contextbridge-web-c5ltxo3mkq-uc.a.run.app"


def run_smoke():
    print("1. Testing frontend landing page...")
    req = urllib.request.urlopen(WEB + "/")
    assert req.status == 200, f"Web status {req.status}"
    print("   -> Frontend landing page 200 OK")

    print("2. Testing frontend demo lesson page...")
    req = urllib.request.urlopen(WEB + "/lesson/demo-binary")
    assert req.status == 200, f"Web lesson status {req.status}"
    print("   -> Frontend demo lesson page 200 OK")

    print("3. Testing backend fixture lesson retrieval...")
    req = urllib.request.urlopen(API + "/analyses/demo-binary")
    assert req.status == 200
    lesson = json.loads(req.read().decode())
    print(f"   -> Lesson: {lesson['title']}")
    print(f"   -> Chapters: {len(lesson['chapters'])}")
    print(f"   -> Contradictions: {len(lesson.get('contradictions', []))}")
    assert len(lesson["chapters"]) >= 5
    assert len(lesson.get("contradictions", [])) >= 1

    print("4. Testing backend Q&A agent on deployed Cloud Run...")
    data = json.dumps({"question": "What feature is introduced on the new Pixel?"}).encode()
    req = urllib.request.Request(
        API + "/analyses/demo-binary/questions",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req)
    assert resp.status == 200
    ans = json.loads(resp.read().decode())
    print(f"   -> Answer text: {ans['text']}")
    assert ans["answer"]["evidenceType"] == "video", f"Expected video, got {ans['answer']['evidenceType']}"
    assert ans["answer"]["evidence"] is not None
    print(f"   -> Evidence: {ans['answer']['evidence']}")
    print(f"   -> Confidence: {ans['answer']['confidence']}")

    print("5. Testing video stream redirect...")

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirect)
    try:
        opener.open(API + "/analyses/demo-binary/video")
    except urllib.error.HTTPError as e:
        assert e.code == 302, f"Expected 302, got {e.code}"
        print(f"   -> Video redirect 302 OK to: {e.headers['Location'][:60]}...")

    print("\nALL DEPLOYED INTEGRATION SMOKE CHECKS PASSED!")


if __name__ == "__main__":
    run_smoke()
