import { useWeb3 } from "@components/providers";
import { ContractAddress } from "..";

export default function Footer() {
  const { contract } = useWeb3();
  console.log(contract);

  return (
    <footer className="bg-gray-900 pt-1">
      <div className="container mx-auto px-6">
        {contract ? (
          <div className="py-5 flex flex-col md:flex-row items-center">
            <p className="text-white text-center text-sm text-primary-2 font-bold flex-1">
              © {new Date().getFullYear()} Rahn Markets
            </p>
            <div className="flex-1">
              <ContractAddress />
            </div>
          </div>
        ) : (
          <div className="py-5 items-center">
            <p className="text-white text-center text-sm text-primary-2 font-bold">
              © {new Date().getFullYear()} Rahn Markets
            </p>
          </div>
        )}
      </div>
    </footer>
  );
}
