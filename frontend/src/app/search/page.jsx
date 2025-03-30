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
        // for testing
        const mockBackendSuggestions = {
          "bread": ["banh mi", "mianbao"],
          "shirt": ["ao", "chen shan"],
        };
        const normalizedQuery = query.toLowerCase();
        const result =
          mockBackendSuggestions[normalizedQuery] || ["No relevant result"];
        await new Promise((resolve) => setTimeout(resolve, 300)); // simulate delay, will delete cos im ocd
        setSuggestions(result);
      };

      fetchSuggestions();
    }
  }, [query]);

  return (
    <main className="p-4 flex flex-col items-center">
      <h1 className="text-xl font-bold mb-4">We also search for "{query}"</h1>

      {suggestions.length > 0 && (
        <div className="bg-white p-3 rounded shadow mb-4 text-center">
          <p className="text-sm text-gray-700 mb-1">Relevant results:</p>
          <ul className="flex gap-2 text-sm text-pink-600 justify-center">
            {suggestions.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Product results can go here */}
    </main>
  );
}