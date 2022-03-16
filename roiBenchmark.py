from utils.livepeer.subgraph import SubgraphQuery, get_earnings_pool
from utils.eth import get_web3_client, get_block, arb_rpc
import csv
from web3 import Web3 
from utils.eth import get_web3_client, get_contract
from utils.livepeer.index import bonding_manager_contract_address
from utils.livepeer.abi.bonding_manager import bonding_manager_contract_abi


round_count = 14
blocks_in_round = 5760
hours_per_year = 8766
hours_per_round = 21
lpt_price = 25
eth_price = 2500
rounds_per_year = 30 # hours_per_year / hours_per_round
subgraphHandler = SubgraphQuery()
filename = "roi_benchmark.csv"

additional_stake = 100

arb_offset = 7375849

w3 = get_web3_client()
contract = get_contract(w3, bonding_manager_contract_address, bonding_manager_contract_abi)
rounds = subgraphHandler.get_recent_rounds(1, round_count)

# data = {
#     "fee_averages": fee_averages,
#     "reward_averages": reward_averages,
#     "fee_medians":fee_medians,
#     "reward_medians": reward_medians
# }
# df = pd.DataFrame(data=data, index=blocks_for_q)

data = {}

def calc_eth_rewards(orch_row):
    print(orch_row["id"], orch_row["round"])

    earnings_pool = get_earnings_pool(contract, Web3.toChecksumAddress(orch_row["id"]), orch_row["round"])
    print(earnings_pool)
    # fraction_of_total_stake = additional_stake / (orch_row["totalStake"] + additional_stake)
    # eth_rewards_per_100 = pending_fees * fraction_of_total_stake
    # print("rewards",eth_rewards_per_100)

    # eth_rewards_usd = eth_price * eth_rewards_per_100
    # print("usd",eth_rewards_usd)
    # investment_usd = (additional_stake * lpt_price)
    # round_roi = ((investment_usd + eth_rewards_usd) - investment_usd) / investment_usd
    # interest_amount = pow((1 + round_roi), rounds_per_year) - 1
    # return [round_roi, interest_amount]

def calc_lpt_inflation(orch_row):
    if int(orch_row["rewardCut"]) == 0:
        return [0,0] 
    
    mintable_tokens = orch_row["total_supply"] * (orch_row["round_inflation"] / 1000000000) # divide by 100m to get percentage
    reward_tokens = (orch_row["totalStake"]  /
                     orch_row["total_active_stake"]) * mintable_tokens
    reward_tokens_less_fee = reward_tokens - (reward_tokens * (orch_row["rewardCut"] / 100))
    
    round_roi = ((orch_row["totalStake"] + reward_tokens_less_fee) - orch_row["totalStake"]) / orch_row["totalStake"]
    interest_amount = pow((1 + round_roi), rounds_per_year) - 1
    return [round_roi, interest_amount]

for round in rounds:
    block = round*blocks_in_round - arb_offset

    round_protocol = subgraphHandler.get_round_protocol(0, 0, {"block": block})

    def orch_map_cb(acc, cur):
        _acc = acc
        for c in cur:
            row = {"round": round, "round_inflation":
                   float(round_protocol["inflation"]), "total_active_stake": float(round_protocol["totalActiveStake"]), "total_supply": float(round_protocol["totalSupply"]), "id": c["id"], "totalStake": float(c["totalStake"]), "feeShare": float(c["feeShare"])/10000, "rewardCut": float(c["rewardCut"])/10000}
            lpt_roi = calc_lpt_inflation(row)
            row["round_lpt_roi"] = lpt_roi[0]
            row["annualized_lpt_roi"] = lpt_roi[1]
            eth_roi = calc_eth_rewards(row)
            # row["round_eth_roi"] = eth_roi[0]
            # row["annualized_eth_roi"] = eth_roi[1]
            _acc.append(row)
        return _acc
    orchestrators = subgraphHandler.paginate_results(
        [], orch_map_cb, subgraphHandler.get_fee_reward, 100, {"block": block})
    
    keys = orchestrators[0].keys()
    csv_write_mode = 'w' if round == rounds[0] else 'a'
    with open(filename, csv_write_mode) as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.DictWriter(csvfile, keys) 

        # only write header on first try
        if csv_write_mode == 'w':
            csvwriter.writeheader()
            
        # writing the data rows 
        csvwriter.writerows(orchestrators)