import React from "react";

function getGreeting() {
  const h = new Date().getHours();
  if (h >= 5  && h < 11) return { text: "Good Morning! Let's find breakfast 🌅", meal: "Breakfast" };
  if (h >= 11 && h < 16) return { text: "Good Afternoon! Time for lunch ☀️",     meal: "Lunch"     };
  if (h >= 16 && h < 21) return { text: "Good Evening! Dinner ideas await 🌙",   meal: "Dinner"    };
  return                         { text: "Late night snack time? 🍎",              meal: "Snack"     };
}

export default function Header() {
  const { text } = getGreeting();
  return (
    <header className="app-header">
      <div className="header-inner">
        <div className="logo">
          <span className="logo-icon">🍳</span>
          <span className="logo-text">RecipeShare</span>
        </div>
        <p className="greeting">{text}</p>
      </div>
    </header>
  );
}
