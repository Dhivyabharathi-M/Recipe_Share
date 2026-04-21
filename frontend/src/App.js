import React, { useState, useCallback } from "react";
import { Toaster, toast } from "react-hot-toast";
import Header        from "./components/Header";
import AddRecipeForm from "./components/AddRecipeForm";
import RecipeList    from "./components/RecipeList";
import Recommendations from "./components/Recommendations";
import Charts        from "./components/Charts";
import { useWebSocket } from "./hooks/useWebSocket";
import "./App.css";

const TABS = ["🍳 Browse", "➕ Add Recipe", "🔍 Recommendations", "📊 Charts"];

export default function App() {
  const [activeTab, setActiveTab]       = useState(0);
  const [refreshKey, setRefreshKey]     = useState(0);

  const onWsMessage = useCallback((msg) => {
    if (msg.event === "new_recipe") {
      toast.success(msg.message || "New Recipe Added!", {
        duration: 4000,
        icon: "🍽️",
        style: { background: "#1a1a2e", color: "#fff", border: "1px solid #e85d04" },
      });
      setRefreshKey((k) => k + 1);
    }
  }, []);

  useWebSocket(onWsMessage);

  const handleCreated = () => {
    setRefreshKey((k) => k + 1);
    setActiveTab(0);
  };

  return (
    <div className="app">
      <Toaster position="top-right" />
      <Header />

      <nav className="tab-nav">
        <div className="tab-nav-inner">
          {TABS.map((tab, i) => (
            <button
              key={tab}
              className={`tab-btn ${activeTab === i ? "tab-active" : ""}`}
              onClick={() => setActiveTab(i)}
            >
              {tab}
            </button>
          ))}
        </div>
      </nav>

      <main className="main-content">
        {activeTab === 0 && <RecipeList refreshTrigger={refreshKey} />}
        {activeTab === 1 && <AddRecipeForm onCreated={handleCreated} />}
        {activeTab === 2 && <Recommendations />}
        {activeTab === 3 && <Charts />}
      </main>

      <footer className="app-footer">
        <p>RecipeShare · Built with FastAPI + React</p>
      </footer>
    </div>
  );
}
