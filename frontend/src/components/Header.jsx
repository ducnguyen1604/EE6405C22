REMOVED_SECRETuse clientREMOVED_SECRET;

import { useState, useEffect } from REMOVED_SECRETreactREMOVED_SECRET;
import { useRouter } from REMOVED_SECRETnext/navigationREMOVED_SECRET;

export default function Header() {
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState(REMOVED_SECRETenREMOVED_SECRET);
  const router = useRouter();

  
  useEffect(() => {
    document.documentElement.setAttribute(REMOVED_SECRETdata-themeREMOVED_SECRET, darkMode ? REMOVED_SECRETdarkREMOVED_SECRET : REMOVED_SECRETlightREMOVED_SECRET);
  }, [darkMode]);

  const handleTitleClick = () => {
    router.push(REMOVED_SECRET/REMOVED_SECRET);
    window.scrollTo({ top: 0, behavior: REMOVED_SECRETsmoothREMOVED_SECRET });
  };

  return (
    <header className=REMOVED_SECRETfixed top-0 left-0 w-full z-50 bg-gray-100/30 dark:bg-gray-800/30 backdrop-blur-md h-16 flex justify-between items-center p-4REMOVED_SECRET>
      <h1
        className=REMOVED_SECRETtext-xl font-bold text-gray-900 dark:text-gray-100 cursor-pointerREMOVED_SECRET
        onClick={handleTitleClick}
      >
        My E-Shop
      </h1>
      <div className=REMOVED_SECRETflex gap-4 items-centerREMOVED_SECRET>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className=REMOVED_SECRETp-2 rounded borderREMOVED_SECRET
        >
          <option value=REMOVED_SECRETenREMOVED_SECRET>English</option>
          <option value=REMOVED_SECRETspREMOVED_SECRET>Spainish</option>
          <option value=REMOVED_SECRETitREMOVED_SECRET>Italian</option>
          <option value=REMOVED_SECRETzhREMOVED_SECRET>中文</option>
        </select>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className=REMOVED_SECRETpx-4 py-2 bg-pink-500 text-white rounded hover:bg-pink-600 active:scale-95 active:bg-pink-700 transition-all duration-150 shadow-md hover:shadow-lgREMOVED_SECRET
        >
          {darkMode ? REMOVED_SECRETLight ModeREMOVED_SECRET : REMOVED_SECRETDark ModeREMOVED_SECRET}
        </button>
      </div>
    </header>
  );
}
