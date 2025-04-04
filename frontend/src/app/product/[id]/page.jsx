import dummyProducts from REMOVED_SECRET@/utils/dummyProductsREMOVED_SECRET;

export default function ProductDetail({ params }) {
  const { id } = params;
  const product = dummyProducts.find((p) => p.id.toString() === id);

  if (!product) {
    return (
      <div className=REMOVED_SECRETp-8 text-center text-gray-600 text-lgREMOVED_SECRET>
        Product not found 😢
      </div>
    );
  }

  return (
    <main className=REMOVED_SECRETcontent-under-header min-h-[calc(100vh-60px)] px-4 py-10 max-w-6xl mx-auto animate-fade-inREMOVED_SECRET>
      <div className=REMOVED_SECRETgrid grid-cols-1 md:grid-cols-2 gap-10REMOVED_SECRET>
        {/* Sticky Image Column */}
        <div className=REMOVED_SECRETmd:sticky md:top-24REMOVED_SECRET>
          <div className=REMOVED_SECRETw-full aspect-square bg-gray-100 flex items-center justify-center rounded-xl shadowREMOVED_SECRET>
            {product.image ? (
              <img
                src={product.image}
                alt={product.name}
                className=REMOVED_SECRETw-full h-full object-cover rounded-xlREMOVED_SECRET
              />
            ) : (
              <span className=REMOVED_SECRETtext-gray-500 text-smREMOVED_SECRET>Image update soon</span>
            )}
          </div>
        </div>

        {/* Info Column */}
        <div className=REMOVED_SECRETflex flex-col gap-6REMOVED_SECRET>
          <h1 className=REMOVED_SECRETtext-4xl font-bold text-pink-700REMOVED_SECRET>{product.name}</h1>
          <p className=REMOVED_SECRETtext-lg text-gray-500 capitalizeREMOVED_SECRET>
            Category: {product.category}
          </p>
          <p className=REMOVED_SECRETtext-base text-gray-700 leading-relaxedREMOVED_SECRET>
            {product.description}
          </p>
          <div className=REMOVED_SECRETflex gap-6 items-center text-sm text-gray-500REMOVED_SECRET>
            <span className=REMOVED_SECRETtext-yellow-500 text-baseREMOVED_SECRET>⭐ {product.rating}</span>
            <span>{product.comments.length} comments</span>
          </div>
          <div className=REMOVED_SECRETtext-3xl font-bold text-pink-600REMOVED_SECRET>${product.price}</div>
          <button className=REMOVED_SECRETmt-2 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 active:scale-95 transition-all shadow-md w-fitREMOVED_SECRET>
            Add to Cart
          </button>
        </div>
      </div>

      {/* Custom CSS animation */}
      
    </main>
  );
}
