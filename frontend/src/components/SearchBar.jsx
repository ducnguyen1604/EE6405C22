REMOVED_SECRETuse clientREMOVED_SECRET;

import { useRouter } from REMOVED_SECRETnext/navigationREMOVED_SECRET;
import { useState, useEffect } from REMOVED_SECRETreactREMOVED_SECRET;

export default function SearchBar({ initialValue = REMOVED_SECRETREMOVED_SECRET }) {
  const [query, setQuery] = useState(initialValue);
  const router = useRouter();

  useEffect(() => {
    setQuery(initialValue); // update if URL query changes
  }, [initialValue]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() !== REMOVED_SECRETREMOVED_SECRET) {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <form
      onSubmit={handleSearch}
      className=REMOVED_SECRETflex flex-col sm:flex-row gap-4 justify-center items-center w-full px-4 max-w-2xlREMOVED_SECRET
    >
      <input
        type=REMOVED_SECRETtextREMOVED_SECRET
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder=REMOVED_SECRETSearch for products...REMOVED_SECRET
        className=REMOVED_SECRETborder border-pink-300 p-4 rounded w-full shadow-md text-lgREMOVED_SECRET
      />
      <button
        type=REMOVED_SECRETsubmitREMOVED_SECRET
        className=REMOVED_SECRETbg-pink-500 text-white px-6 py-3 rounded hover:bg-pink-600 active:scale-95 active:bg-pink-700 transition-all duration-150 shadow-lg text-lgREMOVED_SECRET
      >
        Search
      </button>
    </form>
  );
}
