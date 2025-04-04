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
    <section className="pt-16 p-6 md:p-12 bg-pink-50 text-center shadow-inner">
      <section className="p-6 md:p-12 bg-pink-50 text-center shadow-inner">
        {path === "/" && (
          <div className="mb-6">
            <h2 className="text-3xl md:text-5xl font-bold text-pink-700 mb-3">
              🛍️ Welcome to E-shop!
            </h2>
            <p className="text-gray-700 text-sm md:text-lg">
              Search your favorite products in any language
            </p>
          </div>
        )}

        <form
          onSubmit={handleSearch}
          className="flex gap-2 justify-center mb-4 w-full px-4"
        >
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for products..."
            className="border p-3 rounded w-full max-w-md md:max-w-xl lg:max-w-2xl shadow-sm"
          />
          <button
            type="submit"
            className="bg-pink-500 text-white px-4 md:px-6 rounded hover:bg-pink-600 active:scale-95 active:bg-pink-700 transition-all duration-150 shadow-md hover:shadow-lg"
          >
            Search
          </button>
        </form>
      </section>
    </section>
  );
}
