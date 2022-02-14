import { Breadcrumbs } from "@components/ui/common";
import { EthRates, WalletBar } from "@components/ui/web3";

const LINKS = [
  {
    href: "/marketplace",
    text: "Buy",
  },
  {
    href: "/marketplace/courses/owned",
    text: "My Courses",
  },
  {
    href: "/marketplace/courses/manage",
    text: "Manage Courses",
  },
];

export default function MarketplaceHeader() {
  return (
    <>
      <div className="pt-4">
        <WalletBar />
      </div>
      <EthRates />
      <div className="flex flex-row-reverse p-4 sm:px-6 lg:px-8">
        <Breadcrumbs items={LINKS} />
      </div>
    </>
  );
}
