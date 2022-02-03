from web3 import Web3 
from utils.eth import get_web3_client, get_contract
from utils.livepeer.index import bonding_manager_contract_address
from utils.livepeer.subgraph import SubgraphQuery, get_pending_stake, get_pending_fees
from utils.livepeer.abi.bonding_manager import bonding_manager_contract_abi
import csv

w3 = get_web3_client()
contract = get_contract(w3, bonding_manager_contract_address, bonding_manager_contract_abi)

subgraphHandler = SubgraphQuery()

round = subgraphHandler.get_current_round()

page_size = 100

def acc_cb(acc, cur):
    _acc = acc
    for c in cur:
        stake = Web3.fromWei(get_pending_stake(contract, Web3.toChecksumAddress(c["id"]), round), 'ether')
        if c['delegate']:
            _acc.append([c['id'], c['delegate']['id'], stake])
    return _acc

# field names 
fields = ['delegator_address', 'orchestrator_address', 'stake_amt']
initial_acc = []
filename = "current_delegators.csv"

rows = subgraphHandler.paginate_results(initial_acc,acc_cb, subgraphHandler.get_delegators, page_size)

with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)