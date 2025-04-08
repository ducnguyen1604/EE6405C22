REMOVED_SECRETuse clientREMOVED_SECRET;

import { useSearchParams } from REMOVED_SECRETnext/navigationREMOVED_SECRET;
import { useEffect, useState } from REMOVED_SECRETreactREMOVED_SECRET;
import dummyProducts from REMOVED_SECRET../../utils/dummyProductsREMOVED_SECRET;
import ProductCard from REMOVED_SECRET@/components/ProductCardREMOVED_SECRET;
import SearchBar from REMOVED_SECRET@/components/SearchBarREMOVED_SECRET;

export default function SearchPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get(REMOVED_SECRETqREMOVED_SECRET) || REMOVED_SECRETREMOVED_SECRET;
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    if (query) {
      const fetchSuggestions = async () => {
        const mockBackendSuggestions = {
          bread: [REMOVED_SECRETbanh miREMOVED_SECRET, REMOVED_SECRETmianbaoREMOVED_SECRET],
          REMOVED_SECRETmouth sprayREMOVED_SECRET: [REMOVED_SECRET口腔喷雾REMOVED_SECRET, REMOVED_SECRETspray oraleREMOVED_SECRET],
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
    <main className=REMOVED_SECRETcontent-under-header px-4 pb-10 flex flex-col items-center bg-white min-h-screenREMOVED_SECRET>
      <h1 className=REMOVED_SECRETtext-xl font-bold mb-4REMOVED_SECRET>
        Search Results from multilanguages 🌎
      </h1>

      {/* Pass initialValue to persist query in input */}
      <SearchBar initialValue={query} />

      {!isNoResult ? (
        <>
          <div className=REMOVED_SECRETbg-white p-4 rounded shadow mt-6 mb-6 text-center w-full max-w-2xlREMOVED_SECRET>
            <p className=REMOVED_SECRETtext-sm text-gray-700 mb-1REMOVED_SECRET>We also search for:</p>
            <ul className=REMOVED_SECRETflex flex-wrap gap-2 text-sm text-pink-600 justify-centerREMOVED_SECRET>
              {suggestions.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>

          <div className=REMOVED_SECRETgrid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 w-fullREMOVED_SECRET>
            {dummyProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </>
      ) : (
        <p className=REMOVED_SECRETtext-gray-600 mt-8REMOVED_SECRET>
          Sorry, we currently do not have this product 😢
        </p>
      )}
    </main>
  );
}
