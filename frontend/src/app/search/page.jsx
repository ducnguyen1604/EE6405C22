REMOVED_SECRETuse clientREMOVED_SECRET;

import { useSearchParams } from REMOVED_SECRETnext/navigationREMOVED_SECRET;
import { useEffect, useState } from REMOVED_SECRETreactREMOVED_SECRET;

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get(REMOVED_SECRETqREMOVED_SECRET);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    if (query) {
      // API backend call
      const fetchSuggestions = async () => {
        const mockBackendSuggestions = {
          bread: [REMOVED_SECRETbanh miREMOVED_SECRET, REMOVED_SECRETmianbaoREMOVED_SECRET],
          shirt: [REMOVED_SECRETaoREMOVED_SECRET, REMOVED_SECRETchen shanREMOVED_SECRET],
        };
        const normalizedQuery = query.toLowerCase();
        const result =
          mockBackendSuggestions[normalizedQuery] || [REMOVED_SECRETNo relevant resultREMOVED_SECRET];
        await new Promise((resolve) => setTimeout(resolve, 300));
        setSuggestions(result);
      };

      fetchSuggestions();
    }
  }, [query]);

  const isNoResult =
    suggestions.length === 0 || suggestions.includes(REMOVED_SECRETNo relevant resultREMOVED_SECRET);

  return (
    <main className=REMOVED_SECRETp-4 flex flex-col items-centerREMOVED_SECRET>
      <h1 className=REMOVED_SECRETtext-xl font-bold mb-4REMOVED_SECRET>
        Search Results from multilanguages 🌎
      </h1>

      {!isNoResult && (
        <div className=REMOVED_SECRETbg-white p-3 rounded shadow mb-4 text-centerREMOVED_SECRET>
          <p className=REMOVED_SECRETtext-sm text-gray-700 mb-1REMOVED_SECRET>We also search for:</p>
          <ul className=REMOVED_SECRETflex gap-2 text-sm text-pink-600 justify-centerREMOVED_SECRET>
            {suggestions.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {isNoResult && (
        <p className=REMOVED_SECRETtext-gray-600 mt-4REMOVED_SECRET>
          Sorry, we currently do not have this product 😢
        </p>
      )}

      {/* Product results can go here */}
    </main>
  );
}
