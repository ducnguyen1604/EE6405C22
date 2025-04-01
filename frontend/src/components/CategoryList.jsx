"use client";

import { useState, useEffect } from "react";

const products = ["Bread", "Shirt"];

export default function CategoryList() {
  const [displayText, setDisplayText] = useState("");
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
    <div className="text-center my-5">
      <h2 className="text-lg md:text-xl font-semibold">
        Our notable products: <span className="text-pink-600">{displayText}</span>
        <span className="animate-pulse">|</span>
      </h2>
    </div>
  );
}
