import React, { useState, useEffect } from "react";
import { updateRecipe } from "../services/api";
import toast from "react-hot-toast";

const MEAL_TYPES     = ["Breakfast", "Lunch", "Dinner", "Snack"];
const DIETARY_FOCUS  = ["High Protein", "High Carb", "Balanced", "Low Calorie"];

export default function EditRecipeModal({ recipe, onClose, onUpdated }) {
  const [form, setForm]         = useState({
    title: recipe.title,
    steps: recipe.steps,
    image_url: recipe.image_url || "",
    meal_type: recipe.meal_type || "",
    dietary_focus: recipe.dietary_focus || "",
  });
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags]         = useState(recipe.ingredients.split(",").map(i => i.trim()));
  const [loading, setLoading]   = useState(false);

  const handleChange = (e) => setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const addTag = (e) => {
    if ((e.key === "Enter" || e.key === ",") && tagInput.trim()) {
      e.preventDefault();
      const val = tagInput.trim().replace(/,$/, "");
      if (val && !tags.includes(val)) setTags((t) => [...t, val]);
      setTagInput("");
    }
  };
  
  const removeTag = (t) => setTags((prev) => prev.filter((x) => x !== t));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title.trim())   return toast.error("Title is required");
    if (tags.length === 0)    return toast.error("Add at least one ingredient");
    if (!form.steps.trim())   return toast.error("Steps are required");

    setLoading(true);
    try {
      await updateRecipe(recipe.id, {
        ...form,
        ingredients:   tags.join(", "),
        meal_type:     form.meal_type     || undefined,
        dietary_focus: form.dietary_focus || undefined,
      });
      toast.success("Recipe updated! 🍳");
      onUpdated?.();
      onClose();
    } catch (err) {
      const msg = err.response?.data?.detail || "Failed to update recipe";
      toast.error(Array.isArray(msg) ? msg[0]?.msg : msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>✏️ Edit Recipe</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="recipe-form">
          <div className="form-group">
            <label>Recipe Title *</label>
            <input name="title" value={form.title} onChange={handleChange}
                   placeholder="e.g. Spaghetti Bolognese" required />
          </div>

          <div className="form-group">
            <label>Image URL <span className="hint">(Link to recipe image)</span></label>
            <input name="image_url" value={form.image_url} onChange={handleChange}
                   placeholder="https://example.com/image.jpg" type="url" />
          </div>

          <div className="form-group">
            <label>Ingredients * <span className="hint">(Press Enter or comma to add)</span></label>
            <div className="tag-input-wrapper">
              {tags.map((t) => (
                <span key={t} className="chip">
                  {t}
                  <button type="button" onClick={() => removeTag(t)} className="chip-remove">×</button>
                </span>
              ))}
              <input
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={addTag}
                placeholder={tags.length ? "" : "tomato, pasta, garlic…"}
                className="tag-inner-input"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Steps *</label>
            <textarea name="steps" value={form.steps} onChange={handleChange}
                      rows={4} placeholder="Step 1: Boil water…" required />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Meal Type <span className="hint">(auto-detected if blank)</span></label>
              <select name="meal_type" value={form.meal_type} onChange={handleChange}>
                <option value="">Auto</option>
                {MEAL_TYPES.map((m) => <option key={m}>{m}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Dietary Focus <span className="hint">(auto-tagged if blank)</span></label>
              <select name="dietary_focus" value={form.dietary_focus} onChange={handleChange}>
                <option value="">Auto</option>
                {DIETARY_FOCUS.map((d) => <option key={d}>{d}</option>)}
              </select>
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-outline" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "Updating…" : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
