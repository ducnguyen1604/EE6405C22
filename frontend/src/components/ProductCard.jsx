REMOVED_SECRETuse clientREMOVED_SECRET;

import Link from REMOVED_SECRETnext/linkREMOVED_SECRET;

export default function ProductCard({ product }) {
  // Safely extract multilingual fields
  const name =
    product.name?.en || Object.values(product.name || {})[0] || REMOVED_SECRETUnnamedREMOVED_SECRET;
  const description =
    product.description?.en ||
    Object.values(product.description || {})[0] ||
    REMOVED_SECRETNo descriptionREMOVED_SECRET;
  const image = product.image || REMOVED_SECRET/images/products/default.jpgREMOVED_SECRET;

  return (
    <Link
      href={`/product/${product.id}`}
      className=REMOVED_SECRETborder rounded-xl shadow-sm overflow-hidden bg-white dark:bg-gray-900 hover:shadow-lg hover:scale-[1.04] transition-transform duration-200 w-full max-w-sm flex flex-colREMOVED_SECRET
    >
      {/* Image */}
      <div className=REMOVED_SECRETw-full aspect-[7/6] bg-gray-100 flex items-center justify-centerREMOVED_SECRET>
        {image ? (
          <img
            src={image}
            alt={name}
            className=REMOVED_SECRETw-full h-full object-coverREMOVED_SECRET
          />
        ) : (
          <span className=REMOVED_SECRETtext-gray-500 text-smREMOVED_SECRET>Image update soon</span>
        )}
      </div>

      {/* Info */}
      <div className=REMOVED_SECRETp-4 flex flex-col justify-end flex-1 gap-2REMOVED_SECRET>
        <div className=REMOVED_SECRETflex justify-between items-centerREMOVED_SECRET>
          <h3 className=REMOVED_SECRETfont-semibold text-lg text-gray-900 dark:text-gray-100REMOVED_SECRET>
            {name}
          </h3>
          <span className=REMOVED_SECRETtext-pink-600 font-boldREMOVED_SECRET>${product.price}</span>
        </div>
        <p className=REMOVED_SECRETtext-sm text-gray-500REMOVED_SECRET>{product.category}</p>
        <p className=REMOVED_SECRETtext-sm text-gray-700 dark:text-gray-300 line-clamp-2REMOVED_SECRET>
          {description}
        </p>
        <div className=REMOVED_SECRETflex justify-between items-center mt-2REMOVED_SECRET>
          <span className=REMOVED_SECRETtext-yellow-500 text-smREMOVED_SECRET>⭐ {product.rating}</span>
          <span className=REMOVED_SECRETtext-gray-500 text-xsREMOVED_SECRET>
            {product.comments?.length || 0} comments
          </span>
        </div>
      </div>
    </Link>
  );
}
