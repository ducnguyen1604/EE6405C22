import ProductCard from REMOVED_SECRET../components/ProductCardREMOVED_SECRET;
import dummyProducts from REMOVED_SECRET../utils/dummyProductsREMOVED_SECRET;
import CategoryList from REMOVED_SECRET@/components/CategoryListREMOVED_SECRET;

export default function HomePage() {
  return (
    <main className=REMOVED_SECRETmb-7REMOVED_SECRET>
      <CategoryList />
      <div className=REMOVED_SECRETp-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4REMOVED_SECRET>
        {dummyProducts.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </main>
  );
}
