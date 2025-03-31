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
        // for testing
        const mockBackendSuggestions = {
          REMOVED_SECRETbreadREMOVED_SECRET: [REMOVED_SECRETbanh miREMOVED_SECRET, REMOVED_SECRETmianbaoREMOVED_SECRET],
          REMOVED_SECRETshirtREMOVED_SECRET: [REMOVED_SECRETaoREMOVED_SECRET, REMOVED_SECRETchen shanREMOVED_SECRET],
        };
        const normalizedQuery = query.toLowerCase();
        const result =
          mockBackendSuggestions[normalizedQuery] || [REMOVED_SECRETNo relevant resultREMOVED_SECRET];
        await new Promise((resolve) => setTimeout(resolve, 300)); // simulate delay, will delete cos im ocd
        setSuggestions(result);
      };

      fetchSuggestions();
    }
  }, [query]);

  return (
    <main className=REMOVED_SECRETp-4 flex flex-col items-centerREMOVED_SECRET>
      <h1 className=REMOVED_SECRETtext-xl font-bold mb-4REMOVED_SECRET>Search Results from multilanguages 🌎 </h1>

      {suggestions.length > 0 && (
        <div className=REMOVED_SECRETbg-white p-3 rounded shadow mb-4 text-centerREMOVED_SECRET>
          <p className=REMOVED_SECRETtext-sm text-gray-700 mb-1REMOVED_SECRET>We also search for:</p>
          <ul className=REMOVED_SECRETflex gap-2 text-sm text-pink-600 justify-centerREMOVED_SECRET>
            {suggestions.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Product results can go here */}
    </main>
  );
}