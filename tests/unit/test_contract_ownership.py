from brownie import CourseMarketplace, accounts, config, network, exceptions
from scripts.deploy_eth_marketpalce import deploy_marketplace
from scripts.helper_functions import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest
from operator import itemgetter
import logging
from web3 import Web3

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('deploy_marketplace_fixture')
class TestContractOwnership:

    def test_contract_ownership(self, deploy_marketplace_fixture):
        """Verify contract owner is that who deployed the contract"""
        # Arrange
        contract, expected_contract_owner = itemgetter(
            'contract', 'contract_owner')(deploy_marketplace_fixture)

        # Act
        contract_owner = contract.getContractOwner()

        # Assert
        assert expected_contract_owner == contract_owner, "Contract owner does not match the contract deployer"

    def test_transfer_ownership_fail(self, deploy_marketplace_fixture):
        """Verify non-contract owner CANNOT transfer ownership"""
        # Arrange
        contract, expected_contract_owner = itemgetter(
            'contract', 'contract_owner')(deploy_marketplace_fixture)
        malicious_actor = get_account(index=1)

        # Act
        # transfer ownership should fail!
        with pytest.raises(exceptions.VirtualMachineError):
            contract.transferOwnership(str(malicious_actor), {
                'from': malicious_actor})
        contract_owner = contract.getContractOwner()

        # Assert
        assert contract_owner == expected_contract_owner, "Contract owner does not match expected"

    def test_transfer_ownership_success(self, deploy_marketplace_fixture):
        """Verify contract owner CAN transfer ownership"""
        # Arrange
        contract, contract_owner = itemgetter(
            'contract', 'contract_owner')(deploy_marketplace_fixture)
        expected_transfered_owner = get_account(index=1)

        # Act
        contract.transferOwnership(str(expected_transfered_owner), {
            'from': contract_owner})
        new_contract_owner = contract.getContractOwner()

        # Assert
        assert new_contract_owner == expected_transfered_owner, "Contract ownership was not properly transfered"
