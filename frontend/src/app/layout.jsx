import "./globals.css";
import Header from "../components/Header";
import Footer from "../components/Footer";
import SearchSection from "../components/SearchSection";


export const metadata = {
  title: "My E-Shop",
  description: "Search and browse products easily",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Header />
        <SearchSection />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
