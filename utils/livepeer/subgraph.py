import requests
from web3 import Web3

livepeer_subgraph_url = 'https://api.thegraph.com/subgraphs/name/livepeer/livepeer'

def paginate_results(acc, acc_cb, query_cb, page_size):
    offset = 0
    _continue = True
    while _continue:
        cur = query_cb(offset, page_size)
        acc = acc_cb(acc, cur)
        if(len(cur)) < page_size:
            _continue = False
        else: 
            print("paginating ({offset})....".format(offset=offset))
        offset += page_size   
    return acc

def run_query(q):
    request = requests.post(livepeer_subgraph_url,
                            json={'query': q})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed - existing. Status {}. Query supplied: {}'.format(request.status_code, q))

def get_pending_fees(contract, delegator_address, current_round):
    return contract.caller.pendingFees(Web3.toChecksumAddress(delegator_address), current_round)

def get_pending_stake(contract, delegator_address, current_round):
    return contract.caller.pendingStake(Web3.toChecksumAddress(delegator_address), current_round)

def get_delegators(offset, page_size):
    result = run_query(_get_delegators_query(page_size, offset))
    return result["data"]["delegators"]

def _get_delegators_query(limit, skip):
    return "{ delegators(first: %s, skip: %s) { id delegate { id } } }" % (limit, skip)


def get_current_round():
    query = "{ rounds(first: 1, orderBy: startBlock, orderDirection: desc) { id } }"
    result = run_query(query)
    return int(result["data"]["rounds"][0]["id"])