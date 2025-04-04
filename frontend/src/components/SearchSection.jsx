"use client";

import { useRouter, usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import SearchBar from "@/components/SearchBar";

const suggestions = [
  "bánh mì",
  "pan dulce",
  "croissant",
  "baguette",
  "pão de queijo",
];

export default function SearchSection() {
  const [query, setQuery] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [index, setIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const router = useRouter();
  const path = usePathname();

  useEffect(() => {
    const current = suggestions[index];
    const timeout = setTimeout(() => {
      if (isDeleting) {
        if (charIndex > 0) {
          setCharIndex((prev) => prev - 1);
          setDisplayText(current.substring(0, charIndex - 1));
        } else {
          setIsDeleting(false);
          setIndex((prev) => (prev + 1) % suggestions.length);
        }
      } else {
        if (charIndex < current.length) {
          setCharIndex((prev) => prev + 1);
          setDisplayText(current.substring(0, charIndex + 1));
        } else {
          setTimeout(() => setIsDeleting(true), 2000);
        }
      }
    }, isDeleting ? 50 : 120);

    return () => clearTimeout(timeout);
  }, [charIndex, isDeleting, index]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() !== "") {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <section className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-pink-50 text-center shadow-inner">
      <div className="max-w-4xl w-full p-6 md:p-12">
        {path === "/" && (
          <div className="mb-8">
            <h2 className="text-4xl md:text-6xl font-bold text-pink-700 mb-4">
              🛍️ Welcome to E-shop!
            </h2>
            <p className="text-gray-700 text-lg md:text-2xl">
              Search your favorite products in any language
            </p>
            <p className="text-gray-500 text-md md:text-xl mt-2 italic min-h-[1.5em]">
              Try:{" "}
              <span className="text-pink-500 font-semibold">
                {displayText}
                <span className="blinking-cursor">|</span>
              </span>
            </p>
          </div>
        )}

        {/* Reusable search bar here */}
        <SearchBar className="mx-auto" />
      </div>
      <style jsx>{`
        .blinking-cursor {
          animation: blink 1s infinite;
        }

        @keyframes blink {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0;
          }
        }
      `}</style>
    </section>
  );
}
