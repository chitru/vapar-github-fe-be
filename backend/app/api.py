
from fastapi.routing import APIRouter
from functions import search_repos, repo_details
from schema import Repo, RepoDetails

router = APIRouter()


@router.get("/repos", response_model=list[Repo])
def get_repos(query: str, per_page: int = 20):
    """
    Search and get repositories from GitHub.

    Args: \n
        query (str): The search query. \n
        per_page (int): The number of repositories to return per page. Default is 20.
    """
    return search_repos(query, per_page)


@router.get("/repos/{owner}/{repo}", response_model=RepoDetails)
def get_repo_details(owner: str, repo: str):
    """
    Get details of a repository from GitHub.

    Args: \n
        owner (str): The owner of the repository. \n
        repo (str): The name of the repository.
    """
    return repo_details(owner, repo)
