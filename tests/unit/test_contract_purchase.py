from brownie import CourseMarketplace, accounts, config, network, exceptions
from scripts.deploy_eth_marketpalce import deploy_marketplace
from scripts.helper_functions import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest
from operator import itemgetter
import logging
from web3 import Web3

logger = logging.getLogger(__name__)

PURCHASE_DATA = {
    'course_id': '0x00000000000000000000000000003130',
    'proof': '0x0000000000000000000000000000313000000000000000000000000000003130',
    'value': '900000000'
}


@pytest.mark.parametrize('purchase_course_fixture', [PURCHASE_DATA], indirect=True, scope="class")
@pytest.mark.usefixtures('purchase_course_fixture')
@pytest.mark.usefixtures('deploy_marketplace_fixture')
class TestContractPurchase:

    def test_purchase_course_hash(self, deploy_marketplace_fixture, purchase_course_fixture):
        """Ensure the course hash of a purchased course aligns with what is expected"""
        # Arrange
        contract = itemgetter('contract')(deploy_marketplace_fixture)
        buyer, course_id = itemgetter(
            'buyer', 'course_id')(purchase_course_fixture)
        expected_hash = Web3.solidityKeccak(
            ['bytes16', 'address'], [course_id, str(buyer)])

        # Act
        course_hash = contract.getCourseHash(0)  # get course hash at index 0

        # Assert
        assert expected_hash == course_hash, 'Hash of purchased course does not match expected hash'

    def test_purchased_data(self, deploy_marketplace_fixture, purchase_course_fixture):
        """Verify the data of the purchased course is what is expected"""
        # Arrange
        expected_index = 0
        expected_state = 0
        contract = itemgetter('contract')(deploy_marketplace_fixture)
        price, proof, buyer = itemgetter(
            'value', 'proof', 'buyer')(purchase_course_fixture)

        # Act
        course_hash = contract.getCourseHash(0)  # get course hash at index 0
        course = dict(contract.getCourseByHash(course_hash))

        # Assert
        assert course['id'] == expected_index, f'Course index should be {expected_index}!'
        assert course['price'] == price, f'Course price should be {price}!'
        assert course['proof'] == proof, f'Course proof should be {proof}!'
        assert course['owner'] == buyer, f'Course owner should be {buyer}!'
        assert course['state'] == expected_state, f'Course state should be {expected_state}!'

    def test_repurchase_owned_course(self, deploy_marketplace_fixture, purchase_course_fixture):
        """Should NOT be able to repurchase an already owned course"""
        # Arrange
        contract = itemgetter('contract')(deploy_marketplace_fixture)
        course_id, price, proof, buyer = itemgetter(
            'course_id', 'value', 'proof', 'buyer')(purchase_course_fixture)

        # Act/Assert
        with pytest.raises(exceptions.VirtualMachineError):
            contract.purchaseCourse(course_id, proof, {
                'from': buyer, 'value': price})

    def test_activate_course_fail(self, deploy_marketplace_fixture, purchase_course_fixture):
        """Buyer should NOT be able to activate course """
        # Arrange
        contract = itemgetter('contract')(deploy_marketplace_fixture)
        buyer = itemgetter('buyer')(purchase_course_fixture)
        expected_state = 0  # expected state = 0 : course should fail activation

        # Act
        course_hash = contract.getCourseHash(0)  # get course hash at index 0

        # if buyer tries to activate course, should fail
        with pytest.raises(exceptions.VirtualMachineError):
            contract.activateCourse(course_hash, {'from': buyer})

        course = dict(contract.getCourseByHash(course_hash))

        # Assert
        assert course['state'] == expected_state, 'Course should be in "purchased" state!'

    def test_activate_course_pass(self, deploy_marketplace_fixture):
        """Contract owner SHOULD be able to activate the course """
        # Arrange
        contract, contract_owner = itemgetter(
            'contract', 'contract_owner')(deploy_marketplace_fixture)
        expected_state = 1  # expected state = 1 : course should be in activated state

        # Act
        course_hash = contract.getCourseHash(0)  # get course hash at index 0

        # only contract owner can activate course
        contract.activateCourse(course_hash, {'from': contract_owner})
        course = dict(contract.getCourseByHash(course_hash))

        # Assert
        assert course['state'] == expected_state, 'Course should be in "activated" state!'
