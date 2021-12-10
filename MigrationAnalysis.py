import requests 
from web3 import Web3
from utils.livepeer.abi.bonding_manager import bonding_manager_contract_abi
from utils.eth import get_web3_client, get_contract
from utils.livepeer.subgraph import get_delegators, get_pending_fees, get_pending_stake

wei_conversion_factor = 1000000000000000000
livepeer_round = 2381
min_profitable_lpt_pending_stake = 4
min_profitable_eth_pending_fees = 0.05
page_size = 100


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
contract = get_contract(w3, bonding_manager_contract_address, bonding_manager_contract_abi)
aggregate_eth = 0
aggregate_lpt = 0
eth_impacted = 0
lpt_impacted = 0

_continue = True 
offset = 0
while _continue:
    delegators = get_delegators(offset, page_size)
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
