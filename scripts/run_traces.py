"""One-shot: start server, send 10 requests, flush traces to Langfuse."""
import subprocess
import sys
import time
import json
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
QUERIES = Path("data/sample_queries.jsonl")
PYTHON = sys.executable


def wait_for_server(timeout: int = 15) -> bool:
    for _ in range(timeout):
        try:
            httpx.get(f"{BASE_URL}/health", timeout=1).raise_for_status()
            return True
        except Exception:
            time.sleep(1)
    return False


def main() -> None:
    print("Starting server...")
    server = subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "app.main:app", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if not wait_for_server():
        print("Server failed to start.")
        server.terminate()
        return

    health = httpx.get(f"{BASE_URL}/health").json()
    print(f"Server ready | tracing_enabled={health['tracing_enabled']}")

    lines = [l for l in QUERIES.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"Sending {len(lines)} requests...")
    with httpx.Client(timeout=30) as client:
        for line in lines:
            r = client.post(f"{BASE_URL}/chat", json=json.loads(line))
            data = r.json()
            print(f"  [{r.status_code}] {data.get('correlation_id')} | {json.loads(line)['feature']}")

    print("Flushing traces to Langfuse...")
    from langfuse import get_client
    get_client().flush()
    print("Done — check cloud.langfuse.com > Tracing > Traces (All time)")

    server.terminate()


if __name__ == "__main__":
    main()
