"use client";

import Link from "next/link";

export default function ProductCard({ product }) {
  return (
    <Link
      href={``}
      className="border rounded-xl shadow-sm overflow-hidden bg-white dark:bg-gray-900 hover:shadow-lg hover:scale-[1.04] transition-transform duration-200 w-full max-w-sm flex flex-col"
    >
      {/* Image Part */}
      <div className="w-full aspect-[7/6] bg-gray-100 flex items-center justify-center">
        {product.image ? (
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <span className="text-gray-500 text-sm">Image update soon</span>
        )}
      </div>

      {/* Content Part */}
      <div className="p-4 flex flex-col justify-end flex-1 gap-2">
        <div className="flex justify-between items-center">
          <h3 className="font-semibold text-lg text-gray-900 dark:text-gray-100">
            {product.name}
          </h3>
          <span className="text-pink-600 font-bold">${product.price}</span>
        </div>
        <p className="text-sm text-gray-500">{product.category}</p>
        <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
          {product.description}
        </p>
        <div className="flex justify-between items-center mt-2">
          <span className="text-yellow-500 text-sm">⭐ {product.rating}</span>
          <span className="text-gray-500 text-xs">
            {product.comments.length} comments
          </span>
        </div>
      </div>
    </Link>
  );
}
