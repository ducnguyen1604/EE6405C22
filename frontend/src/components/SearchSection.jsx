REMOVED_SECRETuse clientREMOVED_SECRET;

import { useRouter, usePathname } from REMOVED_SECRETnext/navigationREMOVED_SECRET;
import { useState, useEffect } from REMOVED_SECRETreactREMOVED_SECRET;
import SearchBar from REMOVED_SECRET@/components/SearchBarREMOVED_SECRET;

const suggestions = [
  REMOVED_SECRETbánh mìREMOVED_SECRET,
  REMOVED_SECRETpan dulceREMOVED_SECRET,
  REMOVED_SECRETcroissantREMOVED_SECRET,
  REMOVED_SECRETbaguetteREMOVED_SECRET,
  REMOVED_SECRETpão de queijoREMOVED_SECRET,
];

export default function SearchSection() {
  const [query, setQuery] = useState(REMOVED_SECRETREMOVED_SECRET);
  const [displayText, setDisplayText] = useState(REMOVED_SECRETREMOVED_SECRET);
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
    if (query.trim() !== REMOVED_SECRETREMOVED_SECRET) {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <section className=REMOVED_SECRETmin-h-[calc(100vh-64px)] flex items-center justify-center bg-pink-50 text-center shadow-innerREMOVED_SECRET>
      <div className=REMOVED_SECRETmax-w-4xl w-full p-6 md:p-12REMOVED_SECRET>
        {path === REMOVED_SECRET/REMOVED_SECRET && (
          <div className=REMOVED_SECRETmb-8REMOVED_SECRET>
            <h2 className=REMOVED_SECRETtext-4xl md:text-6xl font-bold text-pink-700 mb-4REMOVED_SECRET>
              🛍️ Welcome to E-shop!
            </h2>
            <p className=REMOVED_SECRETtext-gray-700 text-lg md:text-2xlREMOVED_SECRET>
              Search your favorite products in any language
            </p>
            <p className=REMOVED_SECRETtext-gray-500 text-md md:text-xl mt-2 italic min-h-[1.5em]REMOVED_SECRET>
              Try:{REMOVED_SECRET REMOVED_SECRET}
              <span className=REMOVED_SECRETtext-pink-500 font-semiboldREMOVED_SECRET>
                {displayText}
                <span className=REMOVED_SECRETblinking-cursorREMOVED_SECRET>|</span>
              </span>
            </p>
          </div>
        )}

        {/* Reusable search bar here */}
        <SearchBar className=REMOVED_SECRETmx-autoREMOVED_SECRET />
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
