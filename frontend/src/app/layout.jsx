import REMOVED_SECRET./globals.cssREMOVED_SECRET;
import Header from REMOVED_SECRET../components/HeaderREMOVED_SECRET;
import Footer from REMOVED_SECRET../components/FooterREMOVED_SECRET;
import SearchSection from REMOVED_SECRET../components/SearchSectionREMOVED_SECRET;


export const metadata = {
  title: REMOVED_SECRETMy E-ShopREMOVED_SECRET,
  description: REMOVED_SECRETSearch and browse products easilyREMOVED_SECRET,
};

export default function RootLayout({ children }) {
  return (
    <html lang=REMOVED_SECRETenREMOVED_SECRET>
      <body>
        <Header />
        <SearchSection />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
