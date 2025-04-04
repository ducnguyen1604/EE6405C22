"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import dummyProducts from "../../utils/dummyProducts";
import ProductCard from "@/components/ProductCard";
import SearchBar from "@/components/SearchBar";

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    if (query) {
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
    <main className="pt-24 px-4 pb-10 flex flex-col items-center bg-white min-h-screen">
      <h1 className="text-xl font-bold mb-4">
        Search Results from multilanguages 🌎
      </h1>

      {/* Pass initialValue to persist query in input */}
      <SearchBar initialValue={query} />

      {!isNoResult ? (
        <>
          <div className="bg-white p-4 rounded shadow mt-6 mb-6 text-center w-full max-w-2xl">
            <p className="text-sm text-gray-700 mb-1">We also search for:</p>
            <ul className="flex flex-wrap gap-2 text-sm text-pink-600 justify-center">
              {suggestions.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full">
            {dummyProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </>
      ) : (
        <p className="text-gray-600 mt-8">
          Sorry, we currently do not have this product 😢
        </p>
      )}
    </main>
  );
}
