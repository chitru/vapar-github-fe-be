from pydantic import BaseModel
from typing import Optional


class Repo(BaseModel):
    owner: Optional[str] = None
    repo_name: Optional[str] = None
    full_name: str
    html_url: str
    description: Optional[str] = None
    stargazers_count: int
    forks_count: int
    private: Optional[bool] = None
    avatar_url: Optional[str] = None
    watchers_count: Optional[int] = None


class RepoDetails(BaseModel):
    full_name: str
    name: str
    description: Optional[str] = None
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    language: Optional[str] = None
    license: Optional[dict] = None
    repos_url: str
