import requests
from web3 import Web3

subgraph_urls = {
    "arbitrum": "tbd",
    "mainnet": 'https://api.thegraph.com/subgraphs/name/livepeer/livepeer',
    "arbitrum-rinkeby": 'https://api.thegraph.com/subgraphs/name/livepeer/arbitrum-rinkeby',
    "rinkeby": 'https://api.thegraph.com/subgraphs/name/livepeer/livepeer-rinkeby'
}

class SubgraphQuery:
    def __init__(self, network="mainnet"):
        self.livepeer_subgraph_url = subgraph_urls[network]

    def paginate_results(self, acc, acc_cb, query_cb, page_size):
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

    def run_query(self, q):
        request = requests.post(self.livepeer_subgraph_url,
                                json={'query': q})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception('Query failed - {}. Status {}. Query supplied: {}'.format(request.reason, request.status_code, q))
    def get_orchestrators(self, offset, page_size):
        result = self.run_query(_get_orchestrators_query(page_size, offset))
        return result["data"]["transcoders"]
    def get_delegators(self,offset, page_size):
        result = self.run_query(_get_delegators_query(page_size, offset))
        return result["data"]["delegators"]
    def get_migrators(self, offset, page_size):
        result = self.run_query( _get_migrators_query(page_size, offset))
        return result["data"]["migrateDelegatorFinalizedEvents"]
    def get_current_round(self):
        query = "{ rounds(first: 1, orderBy: startBlock, orderDirection: desc) { id } }"
        result = self.run_query( query)
        return int(result["data"]["rounds"][0]["id"])




# individual calls
def get_pending_fees(contract, delegator_address, current_round):
    return contract.caller.pendingFees(Web3.toChecksumAddress(delegator_address), current_round)

def get_pending_stake(contract, delegator_address, current_round):
    return contract.caller.pendingStake(Web3.toChecksumAddress(delegator_address), current_round)


# raw graphql
def _get_delegators_query(limit, skip):
    return "{ delegators(first: %s, skip: %s) { id delegate { id } } }" % (limit, skip)

def _get_migrators_query(limit, skip):
    return "{ migrateDelegatorFinalizedEvents(first: %s, skip: %s) { delegate delegatedStake stake l1Addr } }" % (limit, skip)

def _get_orchestrators_query(limit, skip):
    return "{ transcoders(first: %s, skip: %s) { id active totalStake } }" % (limit, skip)

