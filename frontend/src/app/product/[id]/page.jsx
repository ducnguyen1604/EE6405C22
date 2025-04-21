"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function ProductDetail() {
  const { id } = useParams(); // From dynamic route
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    const fetchProduct = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/product/${id}`);
        if (!res.ok) throw new Error("Product not found");
        const data = await res.json();
        setProduct(data);
      } catch (err) {
        console.error(err);
        setProduct(null);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="p-8 text-center text-gray-500 text-lg">Loading...</div>
    );
  }

  if (!product) {
    return (
      <div className="p-8 text-center text-gray-600 text-lg">
        Product not found 😢
      </div>
    );
  }

  // Extract fields with fallbacks
  const name =
    product.name?.en || Object.values(product.name || {})[0] || "Unnamed";
  const desc =
    product.description?.en ||
    Object.values(product.description || {})[0] ||
    "No description";

  return (
    <main className="content-under-header min-h-[calc(100vh-60px)] px-4 py-10 max-w-6xl mx-auto animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        {/* Sticky Image Column */}
        <div className="md:sticky md:top-24">
          <div className="w-full aspect-square bg-gray-100 flex items-center justify-center rounded-xl shadow">
            {product.image ? (
              <img
                src={product.image}
                alt={name}
                className="w-full h-full object-cover rounded-xl"
              />
            ) : (
              <span className="text-gray-500 text-sm">Image update soon</span>
            )}
          </div>
        </div>

        {/* Info Column */}
        <div className="flex flex-col gap-6">
          <h1 className="text-4xl font-bold text-pink-700">{name}</h1>
          <p className="text-lg text-gray-500 capitalize">
            Category: {product.category}
          </p>
          <p className="text-base text-gray-700 leading-relaxed">{desc}</p>
          <div className="flex gap-6 items-center text-sm text-gray-500">
            <span className="text-yellow-500 text-base">
              ⭐ {product.rating}
            </span>
            <span>{product.comments?.length || 0} comments</span>
          </div>
          <div className="text-3xl font-bold text-pink-600">
            ${product.price}
          </div>
          <button className="mt-2 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 active:scale-95 transition-all shadow-md w-fit">
            Add to Cart
          </button>
        </div>
      </div>

      {/* Comment Section */}
      <section className="mt-16">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          What our guests say 💬
        </h2>
        <div className="space-y-6">
          {(product.comments || []).map((text, i) => {
            const namePool = [
              "Peach",
              "Cloud",
              "Pine",
              "Leaf",
              "Berry",
              "Rain",
              "Sun",
              "Blossom",
            ];
            const emojiPool = ["🍀", "🌸", "🌿", "☁️", "🍓", "🌼", "🌞", "🍃"];
            const username = `${emojiPool[i % emojiPool.length]} Guest ${
              namePool[i % namePool.length]
            }_${Math.floor(Math.random() * 90 + 10)}`;

            const rating = (Math.random() * 1.5 + 3.5).toFixed(1);

            return (
              <div
                key={i}
                className="bg-white rounded-xl shadow p-4 border border-pink-100"
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="font-medium text-pink-600">{username}</span>
                  <span className="text-yellow-500 text-sm">⭐ {rating}</span>
                </div>
                <p className="text-gray-700 text-sm">{text}</p>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}
