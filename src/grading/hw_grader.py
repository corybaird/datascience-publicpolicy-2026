import json
import urllib.request
import urllib.error
import yaml
import os
from pathlib import Path

class HomeworkReviewer:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.token = self._get_token()
        self.repo = self.config["repository"]
        self.notebook_dir = self.config["notebook_dir"]
        self.rules = self.config["grading_rules"]

    def _get_token(self):
        env_path = Path(".env")
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if "GITHUB_TOKEN" in line:
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        return None

    def _github_api(self, endpoint, is_json=True):
        url = f"https://api.github.com/repos/{self.repo}/{endpoint}"
        req = urllib.request.Request(url)
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read().decode("utf-8")
                return json.loads(content) if is_json else content
        except Exception as e:
            print(f"API Error on {endpoint}: {e}")
            return None

    def _find_notebook_path(self, pr_num):
        files = self._github_api(f"pulls/{pr_num}/files")
        if not files:
            return None
        for f in files:
            name = f["filename"]
            if name.startswith(self.notebook_dir) and name.endswith(".ipynb"):
                return name
        return None

    def _fetch_notebook(self, ref, notebook_path):
        import base64
        import urllib.parse
        endpoint = f"contents/{urllib.parse.quote(notebook_path)}?ref={ref}"
        data = self._github_api(endpoint)
        if not data or "content" not in data:
            return None
        try:
            content = base64.b64decode(data["content"]).decode("utf-8")
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing notebook for ref {ref}: {e}")
            return None

    def grade_notebook(self, notebook):
        code_cells = [cell["source"] for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]
        full_code = "\n".join(["".join(src) if isinstance(src, list) else src for src in code_cells])
        
        score = 0
        total = 0
        feedback = []
        
        for rule in self.rules:
            points = rule["points"]
            total += points
            check = rule["check"]
            desc = rule["description"]
            if check in full_code:
                score += points
                feedback.append(f"  +{points}/{points}: {desc}")
            else:
                feedback.append(f"   0/{points}: MISSING - {desc}")
                
        return score, total, feedback

    def run(self):
        print(f"Starting auto-grader for {self.repo}...")
        prs = self._github_api("pulls?state=all")
        if not prs:
            print("No pull requests found.")
            return

        report_dir = Path("reports/hw")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "hw_1.md"
        
        with open(report_path, "w") as rf:
            rf.write("# HW-1 Auto-Grader Results\n\n")
            rf.write(f"Repository: `{self.repo}`\n\n")

            for pr in prs:
                pr_num = pr["number"]
                student = pr["user"]["login"]
                title = pr["title"]
                ref = pr["head"]["sha"]
                print(f"--- Grading PR #{pr_num} by {student} ---")
                
                rf.write(f"## PR #{pr_num}: {student}\n")
                rf.write(f"- **Title:** {title}\n")
                
                notebook_path = self._find_notebook_path(pr_num)
                if not notebook_path:
                    print(f"  No .ipynb found in {self.notebook_dir}. Skipping.")
                    rf.write(f"- **Error:** No `.ipynb` found in `{self.notebook_dir}`.\n\n")
                    continue

                notebook = self._fetch_notebook(ref, notebook_path)
                if not notebook:
                    print("  Could not fetch or parse notebook. Grade: 0")
                    rf.write(f"- **Notebook:** `{notebook_path}`\n")
                    rf.write("- **Error:** Could not fetch or parse notebook.\n")
                    rf.write("- **Grade:** 0\n\n")
                    continue
                    
                score, total, feedback = self.grade_notebook(notebook)
                print(f"  Notebook: {notebook_path}")
                print(f"  Grade: {score}/{total}")
                
                rf.write(f"- **Notebook:** `{notebook_path}`\n")
                rf.write(f"- **Grade: {score}/{total}**\n\n")
                rf.write("### Feedback\n```text\n")
                
                for line in feedback:
                    print(f"    {line}")
                    rf.write(f"{line}\n")
                    
                rf.write("```\n\n")
                
        print(f"\nReport generated at {report_path}")

if __name__ == "__main__":
    reviewer = HomeworkReviewer("references/configs/hw1_grading.yaml")
    reviewer.run()
