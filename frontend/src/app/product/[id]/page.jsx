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
            <span className=REMOVED_SECRETtext-yellow-500 text-baseREMOVED_SECRET>
              ⭐ {product.rating}
            </span>
            <span>{product.comments.length} comments</span>
          </div>
          <div className=REMOVED_SECRETtext-3xl font-bold text-pink-600REMOVED_SECRET>
            ${product.price}
          </div>
          <button className=REMOVED_SECRETmt-2 bg-pink-500 text-white px-6 py-3 rounded-lg hover:bg-pink-600 active:scale-95 transition-all shadow-md w-fitREMOVED_SECRET>
            Add to Cart
          </button>
        </div>
      </div>

      {/* Comment Section */}
      <section className=REMOVED_SECRETmt-16REMOVED_SECRET>
        <h2 className=REMOVED_SECRETtext-2xl font-bold text-gray-800 mb-6REMOVED_SECRET>
          What our guests say 💬
        </h2>
        <div className=REMOVED_SECRETspace-y-6REMOVED_SECRET>
          {product.comments.map((text, i) => {
            // Generate a creative anonymous username
            const namePool = [
              REMOVED_SECRETPeachREMOVED_SECRET,
              REMOVED_SECRETCloudREMOVED_SECRET,
              REMOVED_SECRETPineREMOVED_SECRET,
              REMOVED_SECRETLeafREMOVED_SECRET,
              REMOVED_SECRETBerryREMOVED_SECRET,
              REMOVED_SECRETRainREMOVED_SECRET,
              REMOVED_SECRETSunREMOVED_SECRET,
              REMOVED_SECRETBlossomREMOVED_SECRET,
            ];
            const emojiPool = [REMOVED_SECRET🍀REMOVED_SECRET, REMOVED_SECRET🌸REMOVED_SECRET, REMOVED_SECRET🌿REMOVED_SECRET, REMOVED_SECRET☁️REMOVED_SECRET, REMOVED_SECRET🍓REMOVED_SECRET, REMOVED_SECRET🌼REMOVED_SECRET, REMOVED_SECRET🌞REMOVED_SECRET, REMOVED_SECRET🍃REMOVED_SECRET];
            const username = `${emojiPool[i % emojiPool.length]} Guest ${
              namePool[i % namePool.length]
            }_${Math.floor(Math.random() * 90 + 10)}`;

            // Generate a random rating between 3.5 and 5.0
            const rating = (Math.random() * 1.5 + 3.5).toFixed(1);

            return (
              <div
                key={i}
                className=REMOVED_SECRETbg-white rounded-xl shadow p-4 border border-pink-100REMOVED_SECRET
              >
                <div className=REMOVED_SECRETflex justify-between items-center mb-1REMOVED_SECRET>
                  <span className=REMOVED_SECRETfont-medium text-pink-600REMOVED_SECRET>{username}</span>
                  <span className=REMOVED_SECRETtext-yellow-500 text-smREMOVED_SECRET>⭐ {rating}</span>
                </div>
                <p className=REMOVED_SECRETtext-gray-700 text-smREMOVED_SECRET>{text}</p>
              </div>
            );
          })}
        </div>
      </section>
    </main>
  );
}
