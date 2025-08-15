import requests
from fastapi import HTTPException
from config import GITHUB_API_BASE

headers = {
    "User-Agent": "github-backend-api/1.0"
}


def search_repos(query: str, per_page: int):
    if not query or not query.strip():
        raise HTTPException(
            status_code=400, detail="Search query cannot be empty")

    if per_page < 1 or per_page > 100:
        raise HTTPException(
            status_code=400, detail="per_page must be between 1 and 100")

    github_api_url = f"{GITHUB_API_BASE}/search/repositories?q={query}&per_page={per_page}"
    response = requests.get(github_api_url, headers=headers)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="No repositories found")
    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)

    try:
        items = response.json()["items"]
        modified_items = []
        for item in items:
            modified_items.append({
                "owner": item["owner"]["login"],
                "repo_name": item["name"],
                "full_name": item["full_name"],
                "html_url": item["html_url"],
                "description": item["description"],
                "stargazers_count": item["stargazers_count"],
                "forks_count": item["forks_count"],
                "private": item["private"],
                "avatar_url": item["owner"]["avatar_url"],
                "watchers_count": item["watchers_count"],
            })
        return modified_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def repo_details(owner: str, repo: str):
    if not owner or not owner.strip():
        raise HTTPException(status_code=400, detail="Owner cannot be empty")
    if not repo or not repo.strip():
        raise HTTPException(
            status_code=400, detail="Repository name cannot be empty")

    github_api_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    response = requests.get(github_api_url, headers=headers)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="No repository found")
    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)

    try:
        data = response.json()
        modified_data = {
            "full_name": data["full_name"],
            "name": data["name"],
            "description": data["description"],
            "stargazers_count": data["stargazers_count"],
            "forks_count": data["forks_count"],
            "open_issues_count": data["open_issues_count"],
            "language": data["language"],
            "license": {"name": data["license"]} if data["license"] else None,
            "repos_url": data["owner"]["html_url"],
        }
        return modified_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
