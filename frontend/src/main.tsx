import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@/index.css";
import App from "@/App.tsx";
import { BrowserRouter, Route, Routes } from "react-router";
import RepoDetails from "@/repos/repodetails";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/repos/:owner/:repo_name" element={<RepoDetails />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
