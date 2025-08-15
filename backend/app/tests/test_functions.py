import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from functions import search_repos, repo_details


class TestSearchRepos:
    """Test cases for search_repos function"""

    @patch('functions.requests.get')
    def test_successful_search_retrieval(self, mock_get):
        """Test successful search retrieval with a valid query"""
        mock_response = Mock()
        mock_response.status_code = 200
        # what we get from github api
        mock_response.json.return_value = {
            "items": [
                {
                    "owner": {"login": "testuser", "avatar_url": "https://example.com/avatar.jpg"},
                    "name": "test-repo",
                    "full_name": "testuser/test-repo",
                    "html_url": "https://github.com/testuser/test-repo",
                    "description": "A test repository",
                    "stargazers_count": 100,
                    "forks_count": 50,
                    "private": False,
                    "watchers_count": 200
                }
            ]
        }
        mock_get.return_value = mock_response

        result = search_repos("test query", 20)

        # Assert the values we get from the function are correct according to the our schema
        assert len(result) == 1
        assert result[0]["owner"] == "testuser"
        assert result[0]["repo_name"] == "test-repo"
        assert result[0]["full_name"] == "testuser/test-repo"
        assert result[0]["description"] == "A test repository"
        assert result[0]["stargazers_count"] == 100
        assert result[0]["forks_count"] == 50
        assert result[0]["private"] is False
        assert result[0]["avatar_url"] == "https://example.com/avatar.jpg"
        assert result[0]["watchers_count"] == 200

        # Verify the request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "search/repositories" in call_args[0][0]

    def test_search_empty_query(self):
        """Test validation for empty query"""
        with pytest.raises(HTTPException) as exc_info:
            search_repos("", 20)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Search query cannot be empty"

    def test_search_invalid_per_page(self):
        """Test validation for invalid per_page values"""
        with pytest.raises(HTTPException) as exc_info:
            search_repos("test", 0)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "per_page must be between 1 and 100"

        with pytest.raises(HTTPException) as exc_info:
            search_repos("test", 101)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "per_page must be between 1 and 100"

    @patch('functions.requests.get')
    def test_search_no_repositories_found(self, mock_get):
        """Test 404 response when no repositories are found"""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        # Test that HTTPException is raised
        with pytest.raises(HTTPException) as exc_info:
            search_repos("nonexistent", 20)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "No repositories found"

    @patch('functions.requests.get')
    def test_search_rate_limit_exceeded(self, mock_get):
        """Test rate limit handling"""
        # Mock 429 response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_get.return_value = mock_response

        # Test that HTTPException is raised
        with pytest.raises(HTTPException) as exc_info:
            search_repos("test", 20)

        assert exc_info.value.status_code == 429
        assert exc_info.value.detail == "Rate limit exceeded"

    @patch('functions.requests.get')
    def test_search_other_error_status(self, mock_get):
        """Test handling of other error status codes"""
        # Mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        # Test that HTTPException is raised
        with pytest.raises(HTTPException) as exc_info:
            search_repos("test", 20)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Internal Server Error"


class TestRepoDetails:
    """Test cases for repo_details function"""

    @patch('functions.requests.get')
    def test_successful_detail_retrieval(self, mock_get):
        """Test successful detail retrieval for a valid repository"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "full_name": "testuser/test-repo",
            "name": "test-repo",
            "description": "A test repository",
            "stargazers_count": 100,
            "forks_count": 50,
            "open_issues_count": 10,
            "language": "Python",
            "license": "MIT License",  # Note: license is a string, not an object
            "owner": {"repos_url": "https://api.github.com/users/testuser/repos"}
        }
        mock_get.return_value = mock_response

        # what we get from github api
        result = repo_details("testuser", "test-repo")

        # Assert the values we get from the function are correct according to the our schema
        assert result["full_name"] == "testuser/test-repo"
        assert result["name"] == "test-repo"
        assert result["description"] == "A test repository"
        assert result["stargazers_count"] == 100
        assert result["forks_count"] == 50
        assert result["open_issues_count"] == 10
        assert result["language"] == "Python"
        assert result["license"]["name"] == "MIT License"
        assert result["repos_url"] == "https://api.github.com/users/testuser/repos"

        # Verify the request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "repos/testuser/test-repo" in call_args[0][0]

    @patch('functions.requests.get')
    def test_repo_details_not_found(self, mock_get):
        """Test 404 for an invalid repository"""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        # Test that HTTPException is raised
        with pytest.raises(HTTPException) as exc_info:
            repo_details("invaliduser", "invalid-repo")

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "No repository found"

    @patch('functions.requests.get')
    def test_repo_details_rate_limit_exceeded(self, mock_get):
        """Test rate limit handling for repo details"""
        # Mock 429 response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_get.return_value = mock_response

        # Test that HTTPException is raised
        with pytest.raises(HTTPException) as exc_info:
            repo_details("testuser", "test-repo")

        assert exc_info.value.status_code == 429
        assert exc_info.value.detail == "Rate limit exceeded"

    @patch('functions.requests.get')
    def test_repo_details_without_license(self, mock_get):
        """Test repository details when license is None"""
        # Mock successful response without license
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "full_name": "testuser/test-repo",
            "name": "test-repo",
            "description": "A test repository",
            "stargazers_count": 100,
            "forks_count": 50,
            "open_issues_count": 10,
            "language": "Python",
            "license": None,
            "owner": {"repos_url": "https://api.github.com/users/testuser/repos"}
        }
        mock_get.return_value = mock_response

        # Call the function
        result = repo_details("testuser", "test-repo")

        # Assertions
        assert result["license"] is None
        assert result["full_name"] == "testuser/test-repo"
        assert result["name"] == "test-repo"
