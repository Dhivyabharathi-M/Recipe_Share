import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ── Recipes ──────────────────────────────────────────────────────────────────
export const createRecipe = (data) => api.post("/recipes/", data);
export const listRecipes  = (params = {}) => api.get("/recipes/", { params });
export const getRecipe    = (id) => api.get(`/recipes/${id}`);
export const updateRecipe = (id, data) => api.put(`/recipes/${id}`, data);
export const deleteRecipe = (id) => api.delete(`/recipes/${id}`);
export const exportRecipe = (id, format = "markdown") =>
  api.get(`/recipes/${id}/export`, { params: { format }, responseType: "blob" });

// ── Recommendations ──────────────────────────────────────────────────────────
export const getRecommendations = (ingredients, topK = 5, timeBased = false) =>
  api.get("/recommendations/", {
    params: { ingredients: ingredients.join(","), top_k: topK, time_based: timeBased },
  });

// ── Stats ─────────────────────────────────────────────────────────────────────
export const getStats = () => api.get("/stats/");

export default api;
