import requests
import time
from config import *
from utils import load_checkpoint, save_checkpoint

def fetch_issues(project,pages):
    start_at = load_checkpoint(project)
    page_count = 0
    while page_count < pages:
        params = {
            "jql": f"project={project}",
            "startAt": start_at,
            "maxResults": PAGE_SIZE,
            "fields": FIELDS
        }
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
                if response.status_code == 429:
                    time.sleep(int(response.headers.get("Retry-After", 60)))
                    continue
                elif response.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                response.raise_for_status()
                data = response.json()
                issues = data.get("issues", [])
                if not issues:
                    return
                yield issues
                start_at += PAGE_SIZE
                page_count += 1
                save_checkpoint(project, start_at)
                break
            except Exception as e:
                print(f"[{project}] Error: {e}")
                time.sleep(2 ** attempt)
               
