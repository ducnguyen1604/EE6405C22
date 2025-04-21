import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";

export default function SearchBar({ initialValue = "", languages = [] }) {
  const [query, setQuery] = useState(initialValue);
  const [langs, setLangs] = useState(languages);
  const router = useRouter();

  useEffect(() => {
    setQuery(initialValue);
  }, [initialValue]);

  useEffect(() => {
    setLangs(languages);
  }, [languages]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() !== "") {
      const langParam = langs.length > 0 ? `&langs=${langs.join(",")}` : "";
      router.push(`/search?q=${encodeURIComponent(query)}${langParam}`);
    }
  };

  return (
    <form
      onSubmit={handleSearch}
      className="flex flex-col sm:flex-row gap-4 justify-center items-center w-full px-4"
    >
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for products..."
        className="border border-pink-300 p-4 rounded w-full max-w-xl shadow-md text-lg"
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
