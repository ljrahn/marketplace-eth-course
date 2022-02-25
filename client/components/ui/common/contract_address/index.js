import { useWeb3 } from "@components/providers";

export default function ContractAddress() {
  const { contract } = useWeb3();
  const contractAddress = contract?._address;

  return contractAddress ? (
    <div className="text-white bg-indigo-600 rounded-md p-2 text-center inline-block">
      <div className="text-black">Contract Address</div>
      {contractAddress}
    </div>
  ) : (
    <></>
  );
}
