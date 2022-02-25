import pytest
from brownie import CourseMarketplace, config, network, exceptions
from scripts.deploy_eth_marketpalce import deploy_marketplace
from scripts.helper_functions import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, create_folder_file_now
import pytest
import logging
from web3 import Web3

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def deploy_marketplace_fixture(request):
    if request.module.__package__ == 'unit':
        if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            pytest.skip()
    elif request.module.__package__ == 'integration':
        if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            pytest.skip()

    contract = deploy_marketplace()

    deploy_data = {
        'contract': contract,
        'contract_owner': get_account(),
    }

    return deploy_data


@pytest.fixture(scope='class')
def purchase_course_fixture(request, deploy_marketplace_fixture):
    buyer = get_account(index=1)

    contract = deploy_marketplace_fixture['contract']
    purchase_data = request.param

    purchase_receipt = contract.purchaseCourse(purchase_data['course_id'], purchase_data['proof'], {
        'from': buyer, 'value': purchase_data['value']})

    purchase_data = purchase_data | {  # merge the purchase data and buyer info into one dict
        'buyer': buyer,
        'purchase_receipt': purchase_receipt
    }
    return purchase_data


def pytest_configure(config):
    """ Create a log file if log_file is not mentioned in *.ini file and add timestamps by directory and on the file.
    ***config.option.htmlpath needs to be fixed and relooked at***"""
    if not config.option.log_file:
        file = create_folder_file_now(directory='logs', file_name='pytest')
        config.option.log_file = file
