import ProductCard from "../components/ProductCard";
import dummyProducts from "../utils/dummyProducts";
import CategoryList from "@/components/CategoryList";

export default function HomePage() {
  return (
    <main className="mb-7">
      <CategoryList />
      <div className="p-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {dummyProducts.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </main>
  );
}
