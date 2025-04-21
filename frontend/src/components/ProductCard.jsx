"use client";

import Link from "next/link";

export default function ProductCard({ product, langs }) {
  const actualProduct = product; // ✅ Handle both flat & nested
  const langList = langs?.split(",").map((l) => l.trim().toLowerCase()) || [];
  // console.log(actualProduct)
  // console.log(langList)
  let name = actualProduct.name?.en || "Unnamed";
  let description = actualProduct.description?.en || "No description";

  // Prioritize selected languages (in order) if available
  for (const lang of langList) {
    if (lang === "chinese" && actualProduct.name?.zh) {
      name = actualProduct.name.zh;
      description = actualProduct.description?.zh || description;
      break;
    }
    if (lang === "spanish" && actualProduct.name?.es) {
      name = actualProduct.name.es;
      description = actualProduct.description?.es || description;
      break;
    }
    if (lang === "italian" && actualProduct.name?.it) {
      name = actualProduct.name.it;
      description = actualProduct.description?.it || description;
      break;
    }
  }

  const image = actualProduct.image || "/images/products/default.jpg";

  return (
    <Link
      href={`/product/${actualProduct.id}`}
      className="border rounded-xl shadow-sm overflow-hidden bg-white dark:bg-gray-900 hover:shadow-lg hover:scale-[1.04] transition-transform duration-200 w-full max-w-sm flex flex-col"
    >
      {/* Image */}
      <div className="w-full aspect-[7/6] bg-gray-100 flex items-center justify-center">
        {image ? (
          <img src={image} alt={name} className="w-full h-full object-cover" />
        ) : (
          <span className="text-gray-500 text-sm">Image update soon</span>
        )}
      </div>

      {/* Info */}
      <div className="p-4 flex flex-col justify-end flex-1 gap-2">
        <div className="flex justify-between items-center">
          <h3 className="font-semibold text-lg text-gray-900 dark:text-gray-100">
            {name}
          </h3>
          <span className="text-pink-600 font-bold">
            ${actualProduct.price}
          </span>
        </div>
        <p className="text-sm text-gray-500">{actualProduct.category}</p>
        <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
          {description}
        </p>
        <div className="flex justify-between items-center mt-2">
          <span className="text-yellow-500 text-sm">
            ⭐ {actualProduct.rating}
          </span>
          <span className="text-gray-500 text-xs">
            {actualProduct.comments?.length || 0} comments
          </span>
        </div>
      </div>
    </Link>
  );
}
