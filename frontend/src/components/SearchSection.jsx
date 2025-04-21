"use client";

import { useRouter, usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import SearchBar from "@/components/SearchBar";

const suggestions = ["Mouth Spray", "口腔喷雾", "aerosol bucal", "spray orale"];

const languages = [
  { name: "English", color: "#c026d3" },
  { name: "Chinese", color: "#ef4444" },
  { name: "Spanish", color: "#f59e0b" },
  { name: "Italian", color: "#10b981" },
];

export default function SearchSection() {
  const [query, setQuery] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [index, setIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [selectedLangs, setSelectedLangs] = useState(["English"]);

  const router = useRouter();
  const path = usePathname();

  useEffect(() => {
    const current = suggestions[index];
    const timeout = setTimeout(
      () => {
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
      },
      isDeleting ? 50 : 120
    );

    return () => clearTimeout(timeout);
  }, [charIndex, isDeleting, index]);

  const toggleLang = (lang) => {
    setSelectedLangs((prev) => {
      // If trying to deselect the last remaining language, prevent it
      if (prev.includes(lang) && prev.length === 1) {
        return prev; // Don't allow removing the last language
      }
      // Normal toggle behavior
      return prev.includes(lang)
        ? prev.filter((l) => l !== lang)
        : [...prev, lang];
    });
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

        {/* Reusable search bar */}
        <SearchBar className="mx-auto" languages={selectedLangs} />

        {/* Language options */}
        <div className="mt-6 text-gray-700 text-lg font-medium">
          You also want to search in:
        </div>
        <div className="mt-3 flex justify-center flex-wrap gap-3">
          {languages.map((lang) => {
            const isSelected = selectedLangs.includes(lang.name);
            return (
              <button
                key={lang.name}
                onClick={() => toggleLang(lang.name)}
                className={`px-4 py-2 rounded-full border-2 font-medium transition-all duration-200 hover:scale-105 active:scale-95 shadow-sm ${
                  isSelected
                    ? "text-white bg-pink-500 border-pink-500"
                    : "text-gray-700 bg-white"
                }`}
                style={{
                  borderColor: lang.color,
                }}
              >
                {lang.name}
              </button>
            );
          })}
        </div>
        <p className="text-sm text-gray-500 mt-2 italic">
          At least one language must be selected (default: English)
        </p>
      </div>

      <style jsx>{`
        .blinking-cursor {
          animation: blink 1s infinite;
        }

        @keyframes blink {
          0%,
          100% {
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
