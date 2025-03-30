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
    <section className=REMOVED_SECRETp-4 bg-pink-50 text-centerREMOVED_SECRET>
      {path === REMOVED_SECRET/REMOVED_SECRET && <h2 className=REMOVED_SECRETtext-xl mb-4REMOVED_SECRET>Welcome to E-shop!</h2>}

      <form onSubmit={handleSearch} className=REMOVED_SECRETflex gap-2 justify-center mb-4REMOVED_SECRET>
        <input
          type=REMOVED_SECRETtextREMOVED_SECRET
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder=REMOVED_SECRETSearch for products...REMOVED_SECRET
          className=REMOVED_SECRETborder p-2 rounded w-full max-w-mdREMOVED_SECRET
        />
        <button type=REMOVED_SECRETsubmitREMOVED_SECRET className=REMOVED_SECRETbg-pink-500 text-white px-4 roundedREMOVED_SECRET>
          Search
        </button>
      </form>
    </section>
  );
}