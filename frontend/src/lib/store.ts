import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Repo } from "./types";

interface SearchState {
  repos: Repo[];
  searchTerm: string;
  currentPage: number;
  loading: boolean;
  error: string;

  setRepos: (repos: Repo[]) => void;
  setSearchTerm: (term: string) => void;
  setCurrentPage: (page: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string) => void;
  clearSearch: () => void;
  resetPage: () => void;
}

export const useSearchStore = create<SearchState>()(
  persist(
    (set) => ({
      repos: [],
      searchTerm: "",
      currentPage: 1,
      loading: false,
      error: "",

      setRepos: (repos) => set({ repos }),
      setSearchTerm: (term) => set({ searchTerm: term }),
      setCurrentPage: (page) => set({ currentPage: page }),
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),

      clearSearch: () =>
        set({
          repos: [],
          searchTerm: "",
          currentPage: 1,
          error: "",
        }),

      resetPage: () => set({ currentPage: 1 }),
    }),
    {
      name: "github-search-storage",
      partialize: () => ({}),
    }
  )
);
