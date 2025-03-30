"use client";

import { useRouter, usePathname, useSearchParams } from "next/navigation";
import { useState } from "react";

export default function SearchSection() {
  const [query, setQuery] = useState("");
  const router = useRouter();
  const path = usePathname();
  const searchParams = useSearchParams();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() !== "") {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <section className="p-4 bg-pink-50 text-center">
      {path === "/" && <h2 className="text-xl mb-4">Welcome to E-shop!</h2>}

      <form onSubmit={handleSearch} className="flex gap-2 justify-center mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for products..."
          className="border p-2 rounded w-full max-w-md"
        />
        <button type="submit" className="bg-pink-500 text-white px-4 rounded">
          Search
        </button>
      </form>
    </section>
  );
}