"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Header() {
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState("en");
  const router = useRouter();

  
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  const handleTitleClick = () => {
    router.push("/");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-gray-100/30 dark:bg-gray-800/30 backdrop-blur-md h-16 flex justify-between items-center p-4">
      <h1
        className="text-xl font-bold text-gray-900 dark:text-gray-100 cursor-pointer"
        onClick={handleTitleClick}
      >
        My E-Shop
      </h1>
      <div className="flex gap-4 items-center">
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="p-2 rounded border"
        >
          <option value="en">English</option>
          <option value="sp">Spainish</option>
          <option value="it">Italian</option>
          <option value="zh">中文</option>
        </select>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="px-4 py-2 bg-pink-500 text-white rounded hover:bg-pink-600 active:scale-95 active:bg-pink-700 transition-all duration-150 shadow-md hover:shadow-lg"
        >
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>
      </div>
    </header>
  );
}
