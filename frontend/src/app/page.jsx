import CategoryList from REMOVED_SECRET../components/CategoryListREMOVED_SECRET;
import ProductCard from REMOVED_SECRET../components/ProductCardREMOVED_SECRET;

export default function HomePage() {
  return (
    <main>
      <CategoryList />
      {/* Example product section */}
      <section className=REMOVED_SECRETp-4 grid grid-cols-2 md:grid-cols-4 gap-4REMOVED_SECRET>
        <ProductCard />
        <ProductCard />
        <ProductCard />
        <ProductCard />
      </section>
    </main>
  );
}
