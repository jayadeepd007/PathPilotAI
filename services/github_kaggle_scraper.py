import requests

class GitHubScraper:
    def __init__(self, username, token=None):
        self.username = username
        self.token = token
        self.base_url = "https://api.github.com"

    def get_repositories(self):
        url = f"{self.base_url}/users/{self.username}/repos"
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        else:
            return []

    def get_repo_details(self, repo_name):
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        # Get repo info
        repo_url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        repo_resp = requests.get(repo_url, headers=headers)
        repo_data = repo_resp.json() if repo_resp.ok else {}
        # Get topics
        topics_url = f"{repo_url}/topics"
        topics_resp = requests.get(topics_url, headers={**headers, "Accept": "application/vnd.github.mercy-preview+json"})
        topics = topics_resp.json().get("names", []) if topics_resp.ok else []
        # Get languages
        lang_url = f"{repo_url}/languages"
        lang_resp = requests.get(lang_url, headers=headers)
        languages = list(lang_resp.json().keys()) if lang_resp.ok else []
        # Get README
        readme_url = f"{repo_url}/readme"
        readme_resp = requests.get(readme_url, headers=headers)
        readme_content = ""
        if readme_resp.ok:
            readme_data = readme_resp.json()
            if "content" in readme_data:
                import base64
                readme_content = base64.b64decode(readme_data["content"]).decode("utf-8", errors="ignore")
        return {
            "name": repo_data.get("name"),
            "description": repo_data.get("description"),
            "topics": topics,
            "languages": languages,
            "readme": readme_content
        }

class KaggleScraper:
    def __init__(self, username, key):
        self.username = username
        self.key = key

    def get_datasets(self):
        url = "https://www.kaggle.com/api/v1/datasets/list"
        headers = {
            "Content-Type": "application/json"
        }
        auth = (self.username, self.key)
        response = requests.get(url, headers=headers, auth=auth)
        if response.ok:
            return response.json()
        else:
            return []

    def get_dataset_details(self, dataset_ref):
        # dataset_ref format: "owner/dataset-name"
        url = f"https://www.kaggle.com/api/v1/datasets/view/{dataset_ref}"
        headers = {
            "Content-Type": "application/json"
        }
        auth = (self.username, self.key)
        response = requests.get(url, headers=headers, auth=auth)
        if response.ok:
            data = response.json()
            return {
                "title": data.get("title"),
                "subtitle": data.get("subtitle"),
                "description": data.get("description"),
                "tags": [tag.get("name") for tag in data.get("tags", [])],
                "size": data.get("totalBytes"),
                "files": [f.get("name") for f in data.get("files", [])]
            }
        else:
            return {}

# Example usage:
if __name__ == "__main__":
    # GitHub
    github_user = "octocat"
    github_token = None  # Optional: your GitHub token
    github_scraper = GitHubScraper(github_user, github_token)
    repos = github_scraper.get_repositories()
    for repo in repos[:2]:  # Limit for demo
        details = github_scraper.get_repo_details(repo["name"])
        print("GitHub Repo Details:", details)

    # Kaggle
    kaggle_user = "your_kaggle_username"
    kaggle_key = "your_kaggle_api_key"
    kaggle_scraper = KaggleScraper(kaggle_user, kaggle_key)
    datasets = kaggle_scraper.get_datasets()
    for ds in datasets[:2]:  # Limit for demo
        ref = ds.get("ref")
        details = kaggle_scraper.get_dataset_details(ref)
        print("Kaggle Dataset Details:", details)