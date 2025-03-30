import CategoryList from "../components/CategoryList";
import ProductCard from "../components/ProductCard";

export default function HomePage() {
  return (
    <main>
      <CategoryList />
      {/* Example product section */}
      <section className="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
        <ProductCard />
        <ProductCard />
        <ProductCard />
        <ProductCard />
      </section>
    </main>
  );
}
