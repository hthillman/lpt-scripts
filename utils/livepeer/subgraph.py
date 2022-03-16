import requests
from web3 import Web3

subgraph_urls = {
    "arbitrum": "https://api.thegraph.com/subgraphs/name/livepeer/arbitrum-one",
    "mainnet": 'https://api.thegraph.com/subgraphs/name/livepeer/livepeer',
    "arbitrum-rinkeby": 'https://api.thegraph.com/subgraphs/name/livepeer/arbitrum-rinkeby',
    "rinkeby": 'https://api.thegraph.com/subgraphs/name/livepeer/livepeer-rinkeby'
}

class SubgraphQuery:
    def __init__(self, network="arbitrum"):
        self.livepeer_subgraph_url = subgraph_urls[network]

    def paginate_results(self, acc, acc_cb, query_cb, page_size, *args):
        offset = 0
        _continue = True
        while _continue:
            cur = query_cb(offset, page_size, *args)
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
    def get_fee_reward(self, offset, page_size, params):
        result = self.run_query(_get_fee_reward_query(page_size, offset, params))
        return result["data"]["transcoders"]
    def get_migrators(self, offset, page_size):
        result = self.run_query( _get_migrators_query(page_size, offset))
        return result["data"]["migrateDelegatorFinalizedEvents"]
    def get_delegator_claim(self, offset, page_size):
        result = self.run_query( _get_delegator_claim_query(page_size, offset))
        return result["data"]["stakeClaimedEvents"]
    def get_recent_rounds(self, offset, page_size):
        result = self.run_query( _get_recent_round_query(page_size, offset))
        return [int(round["id"]) for round in result["data"]["rounds"]]
    def get_round_protocol(self, offset, page_size, params):
        result = self.run_query( _get_round_protocol(page_size, offset, params))
        return result["data"]["protocols"][0]
    def get_recent_rebonds(self, offset, page_size):
        result = self.run_query( _get_recent_rebonds_query(page_size, offset))
        return result["data"]["rebondEvents"]
    def get_recent_rebonds_l1(self, offset, page_size):
        result = self.run_query( _get_recent_rebonds_query_l1(page_size, offset))
        return result["data"]["rebondEvents"]

    def get_current_round(self):
        query = "{ rounds(first: 1, orderBy: startBlock, orderDirection: desc) { id } }"
        result = self.run_query( query)
        return int(result["data"]["rounds"][0]["id"])




# individual calls
def get_pending_fees(contract, delegator_address, current_round):
    return contract.caller.pendingFees(Web3.toChecksumAddress(delegator_address), current_round)

def get_pending_stake(contract, delegator_address, current_round):
    return contract.caller.pendingStake(Web3.toChecksumAddress(delegator_address), current_round)

def get_earnings_pool(contract, delegator_address, current_round):
    return contract.caller.getTranscoderEarningsPoolForRound(Web3.toChecksumAddress(delegator_address), current_round)

# raw graphql
def _get_recent_rebonds_query(limit, skip):
    return "{ rebondEvents (where: {round_gt:\"2468\"}, first: %s, skip: %s){ round { id } amount } }" % (limit, skip)

def _get_recent_rebonds_query_l1(limit, skip):
    return "{ rebondEvents (where: {round_gt:\"2425\"}, first: %s, skip: %s){ round { id } amount } }" % (limit, skip)


def _get_recent_round_query(limit, skip):
    return "{ rounds(orderBy:id, orderDirection: desc, first: %s, skip: %s) { id } }" % (limit, skip)

def _get_delegators_query(limit, skip):
    return "{ delegators(first: %s, skip: %s) { id delegate { id } } }" % (limit, skip)

def _get_migrators_query(limit, skip):
    return "{ migrateDelegatorFinalizedEvents(first: %s, skip: %s) { delegate delegatedStake stake l1Addr } }" % (limit, skip)

def _get_fee_reward_query(limit, skip, params):
    return "{ transcoders(first: %s, skip: %s, block:{number: %s}) { id active totalStake feeShare rewardCut } }" % (limit, skip, params["block"])

def _get_round_protocol(limit, skip, params):
    return "{ protocols( block:{number: %s}) { id inflation totalActiveStake totalSupply } }" % (params["block"])

def _get_orchestrators_query(limit, skip):
    return "{ transcoders(first: %s, skip: %s) { id active totalStake } }" % (limit, skip)

def _get_delegator_claim_query(limit, skip):
    return "{ stakeClaimedEvents(first: %s, skip: %s) { id delegator delegate } }" % (limit, skip)

