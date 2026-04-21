import React, { useState } from "react";
import { getRecommendations } from "../services/api";
import toast from "react-hot-toast";

const BADGE = { "High Protein": "badge-protein", "High Carb": "badge-carb",
                "Balanced": "badge-balanced", "Low Calorie": "badge-low" };

function MatchBar({ score }) {
  return (
    <div className="match-bar-wrap">
      <div className="match-bar" style={{ width: `${score}%` }} />
      <span className="match-label">{score.toFixed(0)}% match</span>
    </div>
  );
}

export default function Recommendations() {
  const [tagInput,   setTagInput]   = useState("");
  const [tags,       setTags]       = useState([]);
  const [results,    setResults]    = useState(null);
  const [timeBased,  setTimeBased]  = useState(false);
  const [topK,       setTopK]       = useState(5);
  const [loading,    setLoading]    = useState(false);

  const addTag = (e) => {
    if ((e.key === "Enter" || e.key === ",") && tagInput.trim()) {
      e.preventDefault();
      const val = tagInput.trim().replace(/,$/, "");
      if (val && !tags.includes(val)) setTags((t) => [...t, val]);
      setTagInput("");
    }
  };
  const removeTag = (t) => setTags((p) => p.filter((x) => x !== t));

  const handleSearch = async () => {
    if (tags.length === 0) { toast.error("Add at least one ingredient"); return; }
    setLoading(true);
    try {
      const res = await getRecommendations(tags, topK, timeBased);
      setResults(res.data);
      if (res.data.length === 0) toast("No matches found. Try different ingredients.", { icon: "🤔" });
    } catch (err) {
      toast.error(err.response?.data?.detail || "Search failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="section-title">🔍 Get Recommendations</h2>

      <div className="form-group">
        <label>Your ingredients <span className="hint">(Press Enter or comma)</span></label>
        <div className="tag-input-wrapper">
          {tags.map((t) => (
            <span key={t} className="chip chip-rec">
              {t}
              <button type="button" onClick={() => removeTag(t)} className="chip-remove">×</button>
            </span>
          ))}
          <input
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyDown={addTag}
            placeholder={tags.length ? "" : "tomato, pasta…"}
            className="tag-inner-input"
          />
        </div>
      </div>

      <div className="rec-options">
        <label className="toggle-label">
          <input type="checkbox" checked={timeBased}
                 onChange={(e) => setTimeBased(e.target.checked)} />
          <span>Filter by current time of day</span>
        </label>
        <label className="toggle-label">
          Top results:
          <select value={topK} onChange={(e) => setTopK(Number(e.target.value))}
                  style={{ marginLeft: 8 }}>
            {[3, 5, 10].map((n) => <option key={n}>{n}</option>)}
          </select>
        </label>
      </div>

      <button className="btn-primary" onClick={handleSearch} disabled={loading}>
        {loading ? "Searching…" : "Find Recipes 🍳"}
      </button>

      {results !== null && (
        <div className="results-section">
          <h3 className="results-title">
            {results.length > 0 ? `${results.length} Recipes Found` : "No matches"}
          </h3>
          {results.map(({ recipe, match_count, match_score, missing_ingredients, substitutions }) => (
            <div key={recipe.id} className="result-card">
              <div className="result-header">
                <div>
                  <h4 className="result-name">{recipe.title}</h4>
                  {recipe.dietary_focus && (
                    <span className={`badge ${BADGE[recipe.dietary_focus] || "badge-balanced"}`}>
                      {recipe.dietary_focus}
                    </span>
                  )}
                </div>
                <span className="match-count">{match_count} matched</span>
              </div>

              <MatchBar score={match_score} />

              <div className="ingredient-chips" style={{ marginTop: 8 }}>
                {recipe.ingredients.split(",").map((i) => (
                  <span key={i} className="ing-chip">{i.trim()}</span>
                ))}
              </div>

              {missing_ingredients.length > 0 && (
                <div className="missing-section">
                  <p className="missing-label">⚠️ Missing: {missing_ingredients.join(", ")}</p>
                  {Object.keys(substitutions).length > 0 && (
                    <ul className="sub-list">
                      {Object.entries(substitutions).map(([k, v]) => (
                        <li key={k}>💡 Missing <b>{k}</b> → Use <b>{v}</b> instead</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}

              <details className="steps-details">
                <summary>View Steps</summary>
                <p className="steps-text">{recipe.steps}</p>
              </details>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
