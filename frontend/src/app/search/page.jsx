"use client";

import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import ProductCard from "@/components/ProductCard";
import SearchBar from "@/components/SearchBar";

const languages = [
  { name: "English", color: "#c026d3" },
  { name: "Chinese", color: "#ef4444" },
  { name: "Spanish", color: "#f59e0b" },
  { name: "Italian", color: "#10b981" },
];

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [langs, setLangs] = useState("");
  const [selectedLangs, setSelectedLangs] = useState([""]);
  const [products, setProducts] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const q = searchParams.get("q") || "";
    const l = searchParams.get("langs") || "";
    setQuery(q);
    setLangs(l);

    const defaultSelected = l
      .split(",")
      .map((x) => x.trim())
      .filter((x) => x);
    if (defaultSelected.length > 0) setSelectedLangs(defaultSelected);
  }, [searchParams]);

  useEffect(() => {
    setLangs(selectedLangs.join(","));
  }, [selectedLangs]);

  useEffect(() => {
    if (query && langs) {
      const fetchProducts = async () => {
        setIsLoading(true);
        try {
          const res = await fetch(
            `http://127.0.0.1:8000/search?q=${encodeURIComponent(
              query
            )}&langs=${encodeURIComponent(langs)}`
          );
          const data = await res.json();
          const translationEntries = Object.entries(data.translations || {});
          setSuggestions(translationEntries);
          setProducts(data.products || []);
        } catch (error) {
          console.error("Failed to fetch:", error);
          setProducts([]);
          setSuggestions([]);
        } finally {
          setIsLoading(false);
        }
      };

      fetchProducts();
    }
  }, [query, langs]);

  const toggleLang = (lang) => {
    setSelectedLangs((prev) => {
      if (prev.includes(lang) && prev.length === 1) return prev;
      return prev.includes(lang)
        ? prev.filter((l) => l !== lang)
        : [...prev, lang];
    });
  };

  const isNoResult = !isLoading && products.length === 0;

  return (
    <main className="content-under-header px-4 pb-10 flex flex-col items-center bg-white min-h-screen">
      <h1 className="text-xl font-bold mb-4">
        Search Results from multilanguages 🌎
      </h1>

      <SearchBar initialValue={query} languages={selectedLangs} />


      <div className="mt-4 text-gray-700 text-md font-medium">
        You also want to search in:
      </div>
      <div className="mt-2 flex justify-center flex-wrap gap-3">
        {languages.map((lang) => {
          const isSelected = selectedLangs.includes(lang.name);
          return (
            <button
            type="button"  // 👈 Add this line
            key={lang.name}
            onClick={() => toggleLang(lang.name)}
            className={`px-4 py-2 rounded-full border-2 font-medium transition-all duration-200 hover:scale-105 active:scale-95 shadow-sm ${
              isSelected
                ? "text-white bg-pink-500 border-pink-500"
                : "text-gray-700 bg-white"
            }`}
            style={{ borderColor: lang.color }}
          >
            {lang.name}
          </button>
          
          );
        })}
      </div>

      <p className="text-sm text-gray-500 mt-4">
        Yayy, we have found {products.length} product(s).
      </p>

      {isLoading ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full mt-8">
          {Array(8)
            .fill(0)
            .map((_, i) => (
              <div
                key={i}
                className="h-44 w-full bg-gray-200 animate-pulse rounded-lg"
              ></div>
            ))}
        </div>
      ) : !isNoResult ? (
        <>
          <div className="bg-white p-4 px-5 rounded shadow mt-6 mb-6 text-center w-full max-w-2xl">
            <p className="text-sm text-gray-700 mb-1">We also searched for:</p>
            <ul className="flex flex-col sm:flex-row flex-wrap gap-2 text-sm justify-center">
              {suggestions.length > 0 ? (
                suggestions.map(([lang, word], i) => {
                  const displayText =
                    typeof word === "object" && word !== null
                      ? Object.values(word)[0]
                      : word;
                  return (
                    <li key={i}>
                      <span className="font-medium text-black capitalize">
                        {lang}:
                      </span>{" "}
                      <span className="text-pink-600">{displayText}</span>
                    </li>
                  );
                })
              ) : (
                <li className="text-gray-400">No suggestions available</li>
              )}
            </ul>
          </div>

          <div className="w-full flex justify-center">
            <div className="w-full max-w-screen-xl px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} langs={langs} />
              ))}
            </div>
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
