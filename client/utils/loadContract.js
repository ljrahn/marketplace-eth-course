const MAP_JSON_ENVIRONMENT = process.env.NEXT_PUBLIC_MAP_JSON_ENVIRONMENT;

export const loadContract = async (name, web3) => {
  let res = await fetch(`/artifacts/contracts/${name}.json`);
  const Artifact = await res.json();

  res = await fetch(`/artifacts/deployments/map.json`);
  const contractMapResponse = await res.json();
  const contractAddress = contractMapResponse[MAP_JSON_ENVIRONMENT][name].pop();

  let contract = null;

  try {
    contract = new web3.eth.Contract(Artifact.abi, contractAddress);
  } catch (err) {
    console.error(`Contract ${name} cannot be loaded: ${err}`);
  }

  return contract;
};
