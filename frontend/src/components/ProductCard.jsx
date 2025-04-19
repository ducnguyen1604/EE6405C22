REMOVED_SECRETuse clientREMOVED_SECRET;

import Link from REMOVED_SECRETnext/linkREMOVED_SECRET;

export default function ProductCard({ product }) {
  const actualProduct = product.product || {};  // ✅ Unwrap the nested product

  const name =
    actualProduct.name?.es ||
    actualProduct.name?.zh ||
    actualProduct.name?.it ||
    REMOVED_SECRETUnnamedREMOVED_SECRET;

  const description =
    actualProduct.description?.es ||
    actualProduct.description?.zh ||
    actualProduct.description?.it ||
    REMOVED_SECRETNo descriptionREMOVED_SECRET;

  const image = actualProduct.image || REMOVED_SECRET/images/products/default.jpgREMOVED_SECRET;

  return (
    <Link
      href={`/product/${actualProduct.id}`}
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
          <span className=REMOVED_SECRETtext-pink-600 font-boldREMOVED_SECRET>${actualProduct.price}</span>
        </div>
        <p className=REMOVED_SECRETtext-sm text-gray-500REMOVED_SECRET>{actualProduct.category}</p>
        <p className=REMOVED_SECRETtext-sm text-gray-700 dark:text-gray-300 line-clamp-2REMOVED_SECRET>
          {description}
        </p>
        <div className=REMOVED_SECRETflex justify-between items-center mt-2REMOVED_SECRET>
          <span className=REMOVED_SECRETtext-yellow-500 text-smREMOVED_SECRET>⭐ {actualProduct.rating}</span>
          <span className=REMOVED_SECRETtext-gray-500 text-xsREMOVED_SECRET>
            {actualProduct.comments?.length || 0} comments
          </span>
        </div>
      </div>
    </Link>
  );
}
