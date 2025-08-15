import Loading from "@/components/loading";
import { site_url } from "@/lib/config";
import axios from "axios";
import { Bug, CodeXml, GitFork, Github, Star } from "lucide-react";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import type { RepoDetails } from "@/lib/types";

export default function RepoDetails() {
  const [repoDetails, setRepoDetails] = useState<RepoDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { owner, repo_name } = useParams();

  const fetchRepoDetails = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${site_url}/repos/${owner}/${repo_name}`
      );
      if (response.status === 200) {
        setRepoDetails(response.data);
      } else if (response.status === 429) {
        setError("Rate limit exceeded");
      } else if (response.status === 404) {
        setError("Repository not found");
      } else {
        setError("Something went wrong");
      }

      setRepoDetails(response.data);
    } catch (error: unknown) {
      console.error("error", error);
      setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRepoDetails();
  }, []);

  return (
    <div className="flex flex-col gap-4 max-w-lg mx-auto pt-28 pb-10">
      <div>
        {loading && <Loading />}
        {error && <p>{error}</p>}
        {repoDetails && (
          <div className="flex flex-col gap-2 p-12">
            <h1 className="text-3xl font-bold">{repoDetails.name}</h1>
            <h2 className="text-gray-500 py-4">{repoDetails.description}</h2>
            <div className="flex flex-row gap-6 items-center">
              <div className="flex flex-row gap-2 items-center">
                <Star className="w-4 h-4" />
                {repoDetails.stargazers_count}
              </div>
              <div className="flex flex-row gap-2 items-center">
                <GitFork className="w-4 h-4" />
                {repoDetails.forks_count}
              </div>
              <div className="flex flex-row gap-2 items-center">
                <Bug className="w-4 h-4" />
                {repoDetails.open_issues_count}
              </div>
              <div className="flex flex-row gap-2 items-center">
                <CodeXml className="w-4 h-4" />
                {repoDetails.language}
              </div>
              <div className="flex flex-row gap-2 items-center">
                <Github className="w-4 h-4" />
                <a
                  href={repoDetails.repos_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Github
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
