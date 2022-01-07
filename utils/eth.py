from web3 import Web3

rpc_url = "https://mainnet.infura.io/v3/69dd01c0890246e09bdbcf9fb85a81c1"

def get_web3_client():
    return Web3(Web3.HTTPProvider(rpc_url))

def get_contract(web3_client, address, abi):
    return web3_client.eth.contract(address=address, abi=abi)

def checksum_list(addresses):
    _addresses =[]
    for address in addresses:
        _addresses.append(Web3.toChecksumAddress(address))
    return _addresses
