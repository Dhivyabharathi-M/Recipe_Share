import React, { useState } from "react";
import { deleteRecipe, exportRecipe } from "../services/api";
import EditRecipeModal from "./EditRecipeModal";
import toast from "react-hot-toast";

const BADGE_COLORS = {
  "High Protein": "badge-protein",
  "High Carb":    "badge-carb",
  "Balanced":     "badge-balanced",
  "Low Calorie":  "badge-low",
};
const MEAL_ICONS = { Breakfast: "🌅", Lunch: "☀️", Dinner: "🌙", Snack: "🍎" };

export default function RecipeCard({ recipe, onDeleted, onUpdated }) {
  const [exporting, setExporting] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [currentRecipe, setCurrentRecipe] = useState(recipe);

  const handleDelete = async () => {
    if (!window.confirm(`Delete "${currentRecipe.title}"?`)) return;
    try {
      await deleteRecipe(currentRecipe.id);
      toast.success("Recipe deleted");
      onDeleted?.();
    } catch {
      toast.error("Could not delete recipe");
    }
  };

  const handleEditSuccess = () => {
    onUpdated?.();
    setIsEditOpen(false);
  };

  const handleExport = async (fmt) => {
    setExporting(true);
    try {
      const res  = await exportRecipe(currentRecipe.id, fmt);
      const ext  = fmt === "pdf" ? "pdf" : "md";
      const mime = fmt === "pdf" ? "application/pdf" : "text/markdown";
      const url  = URL.createObjectURL(new Blob([res.data], { type: mime }));
      const a    = document.createElement("a");
      a.href     = url;
      a.download = `${currentRecipe.title}.${ext}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error("Export failed");
    } finally {
      setExporting(false);
    }
  };

  const ingredients = currentRecipe.ingredients.split(",").map((i) => i.trim());

  return (
    <>
      <div className="recipe-card">
        {currentRecipe.image_url && (
          <img src={currentRecipe.image_url} alt={currentRecipe.title} className="recipe-image" onError={(e) => (e.target.style.display = "none")} />
        )}
        
        <div className="recipe-card-header">
          <h3 className="recipe-title">{currentRecipe.title}</h3>
          <div className="recipe-meta">
            {currentRecipe.meal_type && (
              <span className="meal-tag">
                {MEAL_ICONS[currentRecipe.meal_type]} {currentRecipe.meal_type}
              </span>
            )}
            {currentRecipe.dietary_focus && (
              <span className={`badge ${BADGE_COLORS[currentRecipe.dietary_focus] || "badge-balanced"}`}>
                {currentRecipe.dietary_focus}
              </span>
            )}
          </div>
        </div>

        <div className="ingredient-chips">
          {ingredients.map((ing) => (
            <span key={ing} className="ing-chip">{ing}</span>
          ))}
        </div>

        <details className="steps-details">
          <summary>View Steps</summary>
          <p className="steps-text">{currentRecipe.steps}</p>
        </details>

        <div className="card-actions">
          <button className="btn-sm btn-edit" onClick={() => setIsEditOpen(true)}>
            ✏️ Edit
          </button>
          <button className="btn-sm btn-outline" onClick={() => handleExport("markdown")} disabled={exporting}>
            ⬇ MD
          </button>
          <button className="btn-sm btn-outline" onClick={() => handleExport("pdf")} disabled={exporting}>
            ⬇ PDF
          </button>
          <button className="btn-sm btn-danger" onClick={handleDelete}>🗑 Delete</button>
        </div>

        <p className="created-at">
          Added {new Date(currentRecipe.created_at).toLocaleDateString()}
        </p>
      </div>

      {isEditOpen && (
        <EditRecipeModal
          recipe={currentRecipe}
          onClose={() => setIsEditOpen(false)}
          onUpdated={handleEditSuccess}
        />
      )}
    </>
  );
}
