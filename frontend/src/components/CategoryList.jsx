REMOVED_SECRETuse clientREMOVED_SECRET;

import { useState, useEffect } from REMOVED_SECRETreactREMOVED_SECRET;

const products = [REMOVED_SECRETMouth SprayREMOVED_SECRET, REMOVED_SECRETBreadREMOVED_SECRET, REMOVED_SECRETShirtREMOVED_SECRET];

export default function CategoryList() {
  const [displayText, setDisplayText] = useState(REMOVED_SECRETREMOVED_SECRET);
  const [index, setIndex] = useState(0);
  const [subIndex, setSubIndex] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (index === products.length) {
      setIndex(0);
    }

    const currentWord = products[index];
    const speed = deleting ? 50 : 150;

    const timeout = setTimeout(() => {
      setDisplayText(
        deleting
          ? currentWord.substring(0, subIndex - 1)
          : currentWord.substring(0, subIndex + 1)
      );
      setSubIndex(deleting ? subIndex - 1 : subIndex + 1);

      if (!deleting && subIndex === currentWord.length) {
        setTimeout(() => setDeleting(true), 1000); // pause before deleting
      } else if (deleting && subIndex === 0) {
        setDeleting(false);
        setIndex((prev) => (prev + 1) % products.length);
      }
    }, speed);

    return () => clearTimeout(timeout);
  }, [subIndex, deleting, index]);

  return (
    <div className=REMOVED_SECRETtext-center my-5REMOVED_SECRET>
      <h2 className=REMOVED_SECRETtext-lg md:text-xl font-semiboldREMOVED_SECRET>
        Our notable products: <span className=REMOVED_SECRETtext-pink-600REMOVED_SECRET>{displayText}</span>
        <span className=REMOVED_SECRETanimate-pulseREMOVED_SECRET>|</span>
      </h2>
    </div>
  );
}
