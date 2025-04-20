REMOVED_SECRETuse clientREMOVED_SECRET;

import { useSearchParams, useRouter } from REMOVED_SECRETnext/navigationREMOVED_SECRET;
import { useEffect, useState } from REMOVED_SECRETreactREMOVED_SECRET;
import ProductCard from REMOVED_SECRET@/components/ProductCardREMOVED_SECRET;
import SearchBar from REMOVED_SECRET@/components/SearchBarREMOVED_SECRET;

const languages = [
  { name: REMOVED_SECRETEnglishREMOVED_SECRET, color: REMOVED_SECRET#c026d3REMOVED_SECRET },
  { name: REMOVED_SECRETChineseREMOVED_SECRET, color: REMOVED_SECRET#ef4444REMOVED_SECRET },
  { name: REMOVED_SECRETSpanishREMOVED_SECRET, color: REMOVED_SECRET#f59e0bREMOVED_SECRET },
  { name: REMOVED_SECRETItalianREMOVED_SECRET, color: REMOVED_SECRET#10b981REMOVED_SECRET },
];

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [query, setQuery] = useState(REMOVED_SECRETREMOVED_SECRET);
  const [langs, setLangs] = useState(REMOVED_SECRETREMOVED_SECRET);
  const [selectedLangs, setSelectedLangs] = useState([REMOVED_SECRETREMOVED_SECRET]);
  const [products, setProducts] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const q = searchParams.get(REMOVED_SECRETqREMOVED_SECRET) || REMOVED_SECRETREMOVED_SECRET;
    const l = searchParams.get(REMOVED_SECRETlangsREMOVED_SECRET) || REMOVED_SECRETREMOVED_SECRET;
    setQuery(q);
    setLangs(l);

    const defaultSelected = l
      .split(REMOVED_SECRET,REMOVED_SECRET)
      .map((x) => x.trim())
      .filter((x) => x);
    if (defaultSelected.length > 0) setSelectedLangs(defaultSelected);
  }, [searchParams]);

  useEffect(() => {
    setLangs(selectedLangs.join(REMOVED_SECRET,REMOVED_SECRET));
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
          console.error(REMOVED_SECRETFailed to fetch:REMOVED_SECRET, error);
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
    <main className=REMOVED_SECRETcontent-under-header px-4 pb-10 flex flex-col items-center bg-white min-h-screenREMOVED_SECRET>
      <h1 className=REMOVED_SECRETtext-xl font-bold mb-4REMOVED_SECRET>
        Search Results from multilanguages 🌎
      </h1>

      <SearchBar initialValue={query} languages={selectedLangs} />


      <div className=REMOVED_SECRETmt-4 text-gray-700 text-md font-mediumREMOVED_SECRET>
        You also want to search in:
      </div>
      <div className=REMOVED_SECRETmt-2 flex justify-center flex-wrap gap-3REMOVED_SECRET>
        {languages.map((lang) => {
          const isSelected = selectedLangs.includes(lang.name);
          return (
            <button
            type=REMOVED_SECRETbuttonREMOVED_SECRET  // 👈 Add this line
            key={lang.name}
            onClick={() => toggleLang(lang.name)}
            className={`px-4 py-2 rounded-full border-2 font-medium transition-all duration-200 hover:scale-105 active:scale-95 shadow-sm ${
              isSelected
                ? REMOVED_SECRETtext-white bg-pink-500 border-pink-500REMOVED_SECRET
                : REMOVED_SECRETtext-gray-700 bg-whiteREMOVED_SECRET
            }`}
            style={{ borderColor: lang.color }}
          >
            {lang.name}
          </button>
          
          );
        })}
      </div>

      <p className=REMOVED_SECRETtext-sm text-gray-500 mt-4REMOVED_SECRET>
        Yayy, we have found {products.length} product(s).
      </p>

      {isLoading ? (
        <div className=REMOVED_SECRETgrid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full mt-8REMOVED_SECRET>
          {Array(8)
            .fill(0)
            .map((_, i) => (
              <div
                key={i}
                className=REMOVED_SECRETh-44 w-full bg-gray-200 animate-pulse rounded-lgREMOVED_SECRET
              ></div>
            ))}
        </div>
      ) : !isNoResult ? (
        <>
          <div className=REMOVED_SECRETbg-white p-4 px-5 rounded shadow mt-6 mb-6 text-center w-full max-w-2xlREMOVED_SECRET>
            <p className=REMOVED_SECRETtext-sm text-gray-700 mb-1REMOVED_SECRET>We also searched for:</p>
            <ul className=REMOVED_SECRETflex flex-col sm:flex-row flex-wrap gap-2 text-sm justify-centerREMOVED_SECRET>
              {suggestions.length > 0 ? (
                suggestions.map(([lang, word], i) => {
                  const displayText =
                    typeof word === REMOVED_SECRETobjectREMOVED_SECRET && word !== null
                      ? Object.values(word)[0]
                      : word;
                  return (
                    <li key={i}>
                      <span className=REMOVED_SECRETfont-medium text-black capitalizeREMOVED_SECRET>
                        {lang}:
                      </span>{REMOVED_SECRET REMOVED_SECRET}
                      <span className=REMOVED_SECRETtext-pink-600REMOVED_SECRET>{displayText}</span>
                    </li>
                  );
                })
              ) : (
                <li className=REMOVED_SECRETtext-gray-400REMOVED_SECRET>No suggestions available</li>
              )}
            </ul>
          </div>

          <div className=REMOVED_SECRETw-full flex justify-centerREMOVED_SECRET>
            <div className=REMOVED_SECRETw-full max-w-screen-xl px-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4REMOVED_SECRET>
              {products.map((product) => (
                <ProductCard key={product.id} product={product} langs={langs} />
              ))}
            </div>
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
