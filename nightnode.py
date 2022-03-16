from logging import exception
from utils.eth import get_web3_client, get_contract, buildTransaction, rinkeby
from utils.livepeer.index import bonding_manager_contract_address
from utils.livepeer.abi.bonding_manager import bonding_manager_contract_abi
from web3 import Web3

w3 = get_web3_client(rinkeby)
rinkeby_contract_address =  Web3.toChecksumAddress("0xe42229d764F673EB3FB8B9a56016C2a4DA45ffd7")
contract = get_contract(w3,rinkeby_contract_address, bonding_manager_contract_abi)

newAddress = Web3.toChecksumAddress("0x2955e2342Fd8CcA09291F111C2026A3718502471")
amount = 10
oldDelegate = Web3.toChecksumAddress("0x0e162e354fc65ad1df10605d2f406346a79c71a4")
newDelegate = Web3.toChecksumAddress("0x0e162e354fc65ad1df10605d2f406346a79c71a4")
null_address = "0x0000000000000000000000000000000000000000"
tx = buildTransaction(contract, "transferBond",newAddress, amount,null_address,null_address,null_address,null_address)

private_key = b"<private key should be 32 bytes>"
signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)

w3.eth.send_raw_transaction(signed_txn.rawTransaction)  