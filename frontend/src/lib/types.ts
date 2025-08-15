export interface Repo {
  owner: string | null;
  repo_name: string | null;
  full_name: string;
  html_url: string;
  description: string | null;
  stargazers_count: number;
  forks_count: number;
  private: boolean | null;
  avatar_url: string | null;
  watchers_count: number | null;
}

export interface RepoDetails {
  full_name: string;
  name: string;
  description: string | null;
  stargazers_count: number;
  forks_count: number;
  open_issues_count: number;
  language: string | null;
  license: Record<string, unknown> | null;
  repos_url: string;
}
