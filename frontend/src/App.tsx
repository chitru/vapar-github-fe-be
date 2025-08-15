import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import axios from "axios";
import Loading from "@/components/loading";
import { site_url } from "@/lib/config";
import { Eye, Star } from "lucide-react";
import { Link } from "react-router";
import type { Repo } from "@/lib/types";

function App() {
  const [searchTerm, setSearchTerm] = useState("");

  const [repos, setRepos] = useState<Repo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const searchTerm = formData.get("search") as string;
    setSearchTerm(searchTerm);

    if (searchTerm) {
      setLoading(true);
      try {
        const response = await axios.get(`${site_url}/repos`, {
          params: {
            query: searchTerm,
          },
        });

        if (response.status === 200) {
          setRepos(response.data);
        } else if (response.status === 429) {
          setError("Rate limit exceeded");
        } else if (response.status === 404) {
          setError("Repository not found");
        } else {
          setError("Something went wrong");
        }
      } catch (error: unknown) {
        console.error("error", error);
        setError("Something went wrong");
      } finally {
        setLoading(false);
      }
    } else {
      setError("Please enter a search term");
    }
  };

  return (
    <>
      <div>
        <div className="flex max-w-md gap-2 mx-auto pt-28 pb-10 flex-col bg-white">
          <div>
            <h1 className="text-5xl font-bold tracking-tighter">
              GitHub Repo Search
            </h1>
            <p className="text-gray-500 pt-2">
              Search for a repository on GitHub
            </p>
          </div>
          <form
            className="flex w-full items-center gap-2 mt-10"
            onSubmit={handleSubmit}
          >
            <Input
              type="text"
              name="search"
              placeholder="Search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Button
              type="submit"
              className="bg-black text-white hover:bg-black/70 hover:cursor-pointer"
            >
              Search
            </Button>
          </form>
        </div>
        <div className="flex gap-4 max-w-lg mx-auto px-4 w-full">
          <div className="flex flex-col gap-4 max-w-md mx-auto">
            {loading && <Loading />}
            {error && <p>{error}</p>}
            {repos.map((repo: Repo) => (
              <div key={repo.full_name} className="flex flex-col gap-2">
                <Link
                  className="flex flex-col gap-2 p-4 hover:cursor-pointer hover:bg-gray-50 border rounded-xl border-gray-300"
                  to={`/repos/${repo.owner}/${repo.repo_name}`}
                >
                  <div className="flex flex-row gap-3 items-center">
                    <img
                      src={repo.avatar_url}
                      alt="avatar"
                      className="w-10 h-10 rounded-full object-cover"
                    />
                    <div>
                      <h2 className="font-bold capitalize">{repo.repo_name}</h2>
                      <p className="text-gray-500 text-xs">{repo.owner}</p>
                    </div>
                  </div>
                  <p className="py-4">{repo.description}</p>
                  <div className="flex flex-row gap-6 items-center">
                    <p className="flex flex-row gap-2 items-center">
                      <Star className="w-4 h-4" />
                      {repo.stargazers_count}
                    </p>
                    <p className="flex flex-row gap-2 items-center">
                      <Eye className="w-4 h-4" />
                      {repo.watchers_count}
                    </p>
                  </div>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
