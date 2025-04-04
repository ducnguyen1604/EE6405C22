"use client";

import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

export default function SearchBar({ initialValue = "" }) {
  const [query, setQuery] = useState(initialValue);
  const router = useRouter();

  useEffect(() => {
    setQuery(initialValue); // update if URL query changes
  }, [initialValue]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() !== "") {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <form
      onSubmit={handleSearch}
      className="flex flex-col sm:flex-row gap-4 justify-center items-center w-full px-4 max-w-2xl"
    >
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for products..."
        className="border border-pink-300 p-4 rounded w-full shadow-md text-lg"
      />
      <button
        type="submit"
        className="bg-pink-500 text-white px-6 py-3 rounded hover:bg-pink-600 active:scale-95 active:bg-pink-700 transition-all duration-150 shadow-lg text-lg"
      >
        Search
      </button>
    </form>
  );
}
