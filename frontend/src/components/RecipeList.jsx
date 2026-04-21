import React, { useEffect, useState, useCallback } from "react";
import { listRecipes } from "../services/api";
import RecipeCard from "./RecipeCard";
import toast from "react-hot-toast";

const MEAL_FILTERS = ["All", "Breakfast", "Lunch", "Dinner", "Snack"];

export default function RecipeList({ refreshTrigger }) {
  const [recipes,    setRecipes]    = useState([]);
  const [filter,     setFilter]     = useState("All");
  const [loading,    setLoading]    = useState(true);

  const fetchRecipes = useCallback(async () => {
    setLoading(true);
    try {
      const params = filter !== "All" ? { meal_type: filter } : {};
      const res    = await listRecipes(params);
      setRecipes(res.data);
    } catch {
      toast.error("Could not load recipes");
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => { fetchRecipes(); }, [fetchRecipes, refreshTrigger]);

  return (
    <div className="card">
      <div className="section-header">
        <h2 className="section-title">📋 All Recipes</h2>
        <div className="filter-tabs">
          {MEAL_FILTERS.map((f) => (
            <button
              key={f}
              className={`filter-tab ${filter === f ? "active" : ""}`}
              onClick={() => setFilter(f)}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="loading-grid">
          {[1,2,3].map(i => <div key={i} className="skeleton-card" />)}
        </div>
      ) : recipes.length === 0 ? (
        <div className="empty-state">
          <span>🍽️</span>
          <p>No recipes found. Add one above!</p>
        </div>
      ) : (
        <div className="recipe-grid">
          {recipes.map((r) => (
            <RecipeCard key={r.id} recipe={r} onDeleted={fetchRecipes} onUpdated={fetchRecipes} />
          ))}
        </div>
      )}
    </div>
  );
}
