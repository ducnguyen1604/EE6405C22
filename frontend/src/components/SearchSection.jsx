REMOVED_SECRETuse clientREMOVED_SECRET;

import { useRouter, usePathname, useSearchParams } from REMOVED_SECRETnext/navigationREMOVED_SECRET;
import { useState } from REMOVED_SECRETreactREMOVED_SECRET;

export default function SearchSection() {
  const [query, setQuery] = useState(REMOVED_SECRETREMOVED_SECRET);
  const router = useRouter();
  const path = usePathname();
  const searchParams = useSearchParams();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() !== REMOVED_SECRETREMOVED_SECRET) {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <section className=REMOVED_SECRETpt-16 p-6 md:p-12 bg-pink-50 text-center shadow-innerREMOVED_SECRET>
      <section className=REMOVED_SECRETp-6 md:p-12 bg-pink-50 text-center shadow-innerREMOVED_SECRET>
        {path === REMOVED_SECRET/REMOVED_SECRET && (
          <div className=REMOVED_SECRETmb-6REMOVED_SECRET>
            <h2 className=REMOVED_SECRETtext-3xl md:text-5xl font-bold text-pink-700 mb-3REMOVED_SECRET>
              🛍️ Welcome to E-shop!
            </h2>
            <p className=REMOVED_SECRETtext-gray-700 text-sm md:text-lgREMOVED_SECRET>
              Search your favorite products in any language
            </p>
          </div>
        )}

        <form
          onSubmit={handleSearch}
          className=REMOVED_SECRETflex gap-2 justify-center mb-4 w-full px-4REMOVED_SECRET
        >
          <input
            type=REMOVED_SECRETtextREMOVED_SECRET
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder=REMOVED_SECRETSearch for products...REMOVED_SECRET
            className=REMOVED_SECRETborder p-3 rounded w-full max-w-md md:max-w-xl lg:max-w-2xl shadow-smREMOVED_SECRET
          />
          <button
            type=REMOVED_SECRETsubmitREMOVED_SECRET
            className=REMOVED_SECRETbg-pink-500 text-white px-4 md:px-6 rounded hover:bg-pink-600 active:scale-95 active:bg-pink-700 transition-all duration-150 shadow-md hover:shadow-lgREMOVED_SECRET
          >
            Search
          </button>
        </form>
      </section>
    </section>
  );
}
