import dummyProducts from "@/utils/dummyProducts";

export default function ProductDetail({ params }) {
  const { id } = params;
  const product = dummyProducts.find((p) => p.id.toString() === id);

  if (!product) {
    return (
      <div className="p-8 text-center text-gray-600 text-lg">
        Product not found 😢
      </div>
    );
  }

  return (
    <main className="content-under-header min-h-[calc(100vh-60px)] px-4 py-10 max-w-6xl mx-auto animate-fade-in">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        {/* Sticky Image Column */}
        <div className="md:sticky md:top-24">
          <div className="w-full aspect-square bg-gray-100 flex items-center justify-center rounded-xl shadow">
            {product.image ? (
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-full object-cover rounded-xl"
              />
            ) : (
              <span className="text-gray-500 text-sm">Image update soon</span>
            )}
          </div>
        </div>

        {/* Info Column */}
        <div className="flex flex-col gap-6">
          <h1 className="text-4xl font-bold text-pink-700">{product.name}</h1>
          <p className="text-lg text-gray-500 capitalize">
            Category: {product.category}
          </p>
          <p className="text-base text-gray-700 leading-relaxed">
            {product.description}
          </p>
          <div className="flex gap-6 items-center text-sm text-gray-500">
            <span className="text-yellow-500 text-base">⭐ {product.rating}</span>
            <span>{product.comments.length} comments</span>
          </div>
          <div className="text-3xl font-bold text-pink-600">${product.price}</div>
          <button className="mt-2 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 active:scale-95 transition-all shadow-md w-fit">
            Add to Cart
          </button>
        </div>
      </div>

      {/* Custom CSS animation */}
      
    </main>
  );
}
