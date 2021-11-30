import requests 
from web3 import Web3
from abi import bonding_manager_contract_abi

wei_conversion_factor = 1000000000000000000
livepeer_round = 2381
min_profitable_lpt_pending_stake = 4
min_profitable_eth_pending_fees = 0.05
livepeer_subgraph_url = 'https://api.thegraph.com/subgraphs/name/livepeer/livepeer'
rpc_url = "https://mainnet.infura.io/v3/69dd01c0890246e09bdbcf9fb85a81c1"
bonding_manager_contract_address = '0x511Bc4556D823Ae99630aE8de28b9B80Df90eA2e'
page_size = 100

def run_query(q):
    request = requests.post(livepeer_subgraph_url,
                            json={'query': q})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed - existing. Status {}. Query supplied: {}'.format(request.status_code, q))


def get_query(limit, skip):
    return "{ delegators(first: %s, skip: %s) { id } }" % (limit, skip)

def get_delegators(offset):
    result = run_query(get_query(page_size, offset))
    return result["data"]["delegators"]

def get_web3_client():
    return Web3(Web3.HTTPProvider(rpc_url))

def get_contract(web3_client):
    return web3_client.eth.contract(address=bonding_manager_contract_address, abi=bonding_manager_contract_abi)

def get_pending_fees(contract, delegator_address, current_round):
    return contract.caller.pendingFees(Web3.toChecksumAddress(delegator_address), current_round)

def get_pending_stake(contract, delegator_address, current_round):
    return contract.caller.pendingStake(Web3.toChecksumAddress(delegator_address), current_round)



def get_aggregate_dust(delegators):
    aggregate_eth_fees = 0
    aggregate_pending_stake = 0
    lpt_impacted = 0
    eth_impacted = 0
    for d in delegators:
        pending_eth_fees = Web3.fromWei(get_pending_fees(contract, d["id"], livepeer_round), 'ether')
        if(pending_eth_fees < min_profitable_eth_pending_fees):
            aggregate_eth_fees += pending_eth_fees
            eth_impacted += 1

        pending_stake = Web3.fromWei(get_pending_stake(contract, d["id"], livepeer_round), 'ether')
        if pending_stake < min_profitable_lpt_pending_stake:
            aggregate_pending_stake += pending_stake
            lpt_impacted += 1
    return aggregate_eth_fees, aggregate_pending_stake, eth_impacted, lpt_impacted



w3 = get_web3_client()
contract = get_contract(w3)
aggregate_eth = 0
aggregate_lpt = 0
eth_impacted = 0
lpt_impacted = 0

_continue = True 
offset = 0
while _continue:
    delegators = get_delegators(offset)
    _aggregate_eth, _aggregate_lpt, _eth_impacted, _lpt_impacted =get_aggregate_dust(delegators)
    aggregate_eth += _aggregate_eth
    aggregate_lpt += _aggregate_lpt
    eth_impacted += _eth_impacted
    lpt_impacted += _lpt_impacted
    if(len(delegators)) < page_size:
        _continue = False
    else: 
        print("paginating ({offset})....".format(offset=offset))
    offset += page_size   

print(
    """
    LPT: {aggregate_lpt}
    Delegators Impacted: {lpt_impacted}

    ETH: {aggregate_eth}
    Delegators Impacted: {eth_impacted}

    """.format(aggregate_eth=aggregate_eth, aggregate_lpt=aggregate_lpt, lpt_impacted=lpt_impacted, eth_impacted=eth_impacted)
)
