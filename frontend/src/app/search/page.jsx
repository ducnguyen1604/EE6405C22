"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q");
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    if (query) {
      // API backend call
      const fetchSuggestions = async () => {
        const mockBackendSuggestions = {
          bread: ["banh mi", "mianbao"],
          shirt: ["ao", "chen shan"],
        };
        const normalizedQuery = query.toLowerCase();
        const result =
          mockBackendSuggestions[normalizedQuery] || ["No relevant result"];
        await new Promise((resolve) => setTimeout(resolve, 300));
        setSuggestions(result);
      };

      fetchSuggestions();
    }
  }, [query]);

  const isNoResult =
    suggestions.length === 0 || suggestions.includes("No relevant result");

  return (
    <main className="p-4 flex flex-col items-center">
      <h1 className="text-xl font-bold mb-4">
        Search Results from multilanguages 🌎
      </h1>

      {!isNoResult && (
        <div className="bg-white p-3 rounded shadow mb-4 text-center">
          <p className="text-sm text-gray-700 mb-1">We also search for:</p>
          <ul className="flex gap-2 text-sm text-pink-600 justify-center">
            {suggestions.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {isNoResult && (
        <p className="text-gray-600 mt-4">
          Sorry, we currently do not have this product 😢
        </p>
      )}

      {/* Product results can go here */}
    </main>
  );
}
