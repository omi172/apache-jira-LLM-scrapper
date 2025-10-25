from config import PROJECTS
from scraper import fetch_issues
from transformer import transform_issue, write_jsonl
import os
from config import OUTPUT_DIR,PAGE_SIZE

os.makedirs(OUTPUT_DIR, exist_ok=True)



def run():
    for project in PROJECTS:
        print(f"Scraping {project}...")
        for raw_issues in fetch_issues(project, PAGE_SIZE):
            transformed = [
                transform_issue(issue, project)
                for issue in raw_issues
                if issue and isinstance(issue, dict)
            ]
            write_jsonl(project, transformed)
        print(f"Completed {project}.")


if __name__ == "__main__":
    run()
