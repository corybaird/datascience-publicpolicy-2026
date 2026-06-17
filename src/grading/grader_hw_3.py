import json
import urllib.request
import subprocess
import re
import yaml
import pandas as pd
from pathlib import Path
from posixpath import basename
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from references.dictionaries.GITHUB_MAPPING import GITHUB_TO_STUDENT

class Homework3Grader:
    def __init__(self, config_path="references/configs/hw3_grading.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.repo = self.config["repository"]
        self.notebook_dir = self.config["notebook_dir"]
        self.checklist_path = self.config["checklist_path"]
        self.output_checklist_path = self.config["output_checklist_path"]
        self.output_report_path = self.config["output_report_path"]
        self.hw3_pattern = re.compile(r"(?:hw|homework)[\s_-]*3", re.IGNORECASE)

    def get_token(self):
        try:
            res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        except Exception:
            return None

    def github_api(self, endpoint, token):
        url = f"https://api.github.com/repos/{self.repo}/{endpoint}"
        req = urllib.request.Request(url)
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(f"API Error on {endpoint}: {e}")
            return None

    def get_pr_files(self, pr_num, token):
        return self.github_api(f"pulls/{pr_num}/files", token)

    def get_all_prs(self, token):
        prs = []
        page = 1
        while True:
            batch = self.github_api(f"pulls?state=all&per_page=100&page={page}", token)
            if not batch:
                break
            prs.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return prs

    @staticmethod
    def normalize_name(name):
        return re.sub(r"[^a-z0-9]", "", str(name).lower())

    def is_hw3_title(self, title):
        return bool(self.hw3_pattern.search(title or ""))

    def find_hw3_notebooks(self, files, title):
        notebook_dir = self.notebook_dir.rstrip("/").lower() + "/"
        title_has_hw3 = self.is_hw3_title(title)
        notebooks = []

        for file_info in files or []:
            filename = file_info.get("filename", "")
            if not filename.lower().endswith(".ipynb"):
                continue

            additions = file_info.get("additions")
            if additions is not None and additions <= 0:
                continue

            filename_lower = filename.lower()
            notebook_name = basename(filename_lower)
            in_hw3_dir = filename_lower.startswith(notebook_dir)
            path_has_hw3 = bool(self.hw3_pattern.search(filename_lower))
            name_has_hw3 = bool(self.hw3_pattern.search(notebook_name))

            if in_hw3_dir or path_has_hw3 or (title_has_hw3 and name_has_hw3):
                notebooks.append(filename)

        return notebooks

    def run(self):
        token = self.get_token()
        print(f"Starting Homework 3 check for {self.repo}...")

        prs = self.get_all_prs(token)
        if not prs:
            print("No pull requests found.")
            return

        print(f"Fetched {len(prs)} total pull requests.")
        
        submissions = {}
        unmapped_hw3_users = {}
        lookup = {k.lower(): v for k, v in GITHUB_TO_STUDENT.items()}
        for pr in prs:
            pr_num = pr["number"]
            user = pr["user"]["login"]
            title = pr["title"]
            
            student_name = lookup.get(user.lower())
            if not student_name:
                continue
                
            if student_name in submissions:
                continue
                
            files = self.get_pr_files(pr_num, token)
            if not files:
                continue

            hw3_notebooks = self.find_hw3_notebooks(files, title)
            if hw3_notebooks:
                submissions[student_name] = {
                    "pr_number": pr_num,
                    "user": user,
                    "title": title,
                    "notebooks": hw3_notebooks,
                }
                print(f"Mapped student {student_name} to PR #{pr_num} ({user})")

        for pr in prs:
            user = pr["user"]["login"]
            if user.lower() in lookup:
                continue
            if user in unmapped_hw3_users:
                continue

            files = self.get_pr_files(pr["number"], token)
            hw3_notebooks = self.find_hw3_notebooks(files, pr["title"])
            if hw3_notebooks:
                unmapped_hw3_users[user] = {
                    "pr_number": pr["number"],
                    "title": pr["title"],
                    "notebooks": hw3_notebooks,
                }

        checklist_path = Path(self.checklist_path)
        if not checklist_path.exists():
            print(f"Error: Checklist not found at {checklist_path}")
            return
            
        df = pd.read_csv(checklist_path)
        
        hw3_status = []
        normalized_submissions = {
            self.normalize_name(sub_name): info
            for sub_name, info in submissions.items()
        }
        for index, row in df.iterrows():
            name = row["Student Name"].strip()
            if name in submissions:
                hw3_status.append("✅")
            else:
                status = "✅" if self.normalize_name(name) in normalized_submissions else "❌"
                hw3_status.append(status)
                    
        df["HW3"] = hw3_status
        
        output_csv_path = Path(self.output_checklist_path)
        output_csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_csv_path, index=False)
        print(f"Updated checklist saved to {output_csv_path}")
        
        output_md_path = Path(self.output_report_path)
        output_md_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_md_path, "w", encoding="utf-8") as rf:
            rf.write("# HW-3 PR Submission Results\n\n")
            rf.write(f"Repository: `{self.repo}`\n\n")
            rf.write(f"Total roster submissions found: **{hw3_status.count('✅')} / {len(hw3_status)}**\n\n")
            rf.write("| Student Name | Submitted via PR | PR Details | Notebook Path |\n")
            rf.write("|---|---|---|---|\n")
            
            for index, row in df.iterrows():
                name = row["Student Name"].strip()
                status = row["HW3"]
                if status == "✅":
                    sub_info = submissions.get(name) or normalized_submissions.get(self.normalize_name(name))
                    if sub_info:
                        pr_link = f"PR #{sub_info['pr_number']} ({sub_info['user']}): {sub_info['title']}"
                        notebook_path = "<br>".join(f"`{path}`" for path in sub_info["notebooks"])
                    else:
                        pr_link = "Yes"
                        notebook_path = ""
                else:
                    pr_link = "No submission found"
                    notebook_path = ""
                rf.write(f"| {name} | {status} | {pr_link} | {notebook_path} |\n")

            if unmapped_hw3_users:
                rf.write("\n## Unmapped HW3-Like PRs\n\n")
                rf.write("These PRs include HW3-looking notebooks but do not match the current GitHub-to-student mapping.\n\n")
                rf.write("| GitHub User | PR Details | Notebook Path |\n")
                rf.write("|---|---|---|\n")
                for user, info in sorted(
                    unmapped_hw3_users.items(),
                    key=lambda item: item[1]["pr_number"],
                    reverse=True,
                ):
                    notebook_path = "<br>".join(f"`{path}`" for path in info["notebooks"])
                    rf.write(
                        f"| {user} | PR #{info['pr_number']}: {info['title']} | {notebook_path} |\n"
                    )
                
        print(f"Report generated at {output_md_path}")
        if unmapped_hw3_users:
            print(f"Found {len(unmapped_hw3_users)} unmapped HW3-like PR users.")

if __name__ == "__main__":
    grader = Homework3Grader()
    grader.run()
