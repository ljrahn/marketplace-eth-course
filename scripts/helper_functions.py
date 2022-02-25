from brownie import network, accounts, config
from datetime import datetime
import os

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']
FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).strip('scripts')


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]

    return accounts.add(config['wallets']['from_key'])


def create_folder_file_now(directory=None, file_name=None, file_type='log'):
    """Creates a folder and file path in the form /'directory'/month/day/'file_name'.'file_type'
    :param directory: The directory you wish to stores the folder file path
    :param file_name: The file name
    :param file_type: The file extension eg. 'log', 'png' etc.
    :returns: the full path to the file """
    if directory is None or file_name is None:
        raise FileNotFoundError('Directory or filename was not specified')
    else:
        now = datetime.now()
        os.system(
            f'mkdir -p {os.path.join(ROOT_DIR, directory, now.strftime("%B"), now.strftime("%d"))}')
        file = os.path.join(ROOT_DIR, directory, now.strftime("%B"), now.strftime("%d"),
                            f'{file_name}_{now.strftime("%H")}-{now.strftime("%M")}.{file_type}')

        return file
