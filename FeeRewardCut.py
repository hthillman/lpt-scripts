import argparse
from utils.livepeer.subgraph import SubgraphQuery
from utils.eth import get_web3_client, get_block, arb_rpc
import statistics
import matplotlib.pyplot as plt
import pandas as pd


all_args = argparse.ArgumentParser()

all_args.add_argument("-depth", "--depth", required=True,
   help="integer - # of blocks to look at. query will look at 1/100 blocks")

args = vars(all_args.parse_args())

l2SubgraphHandler = SubgraphQuery()

# l1SubgraphHandler = SubgraphQuery("mainnet")
# eth_mainnet_map = l1SubgraphHandler.paginate_results({}, orch_map_cb, l1SubgraphHandler.get_fee_reward)

w3 = get_web3_client(arb_rpc)
block = int(get_block(w3)["number"])

# offset block to avoid subgraph syncing issues
block_w_offset = block - 100

def orch_map_cb(acc, cur):
    _acc = acc
    for c in cur:
        _acc[c["id"]] = c
    return _acc

arbitrum_maps = []

blocks_for_q = []
for i in range(int(args["depth"])):
    blocks_for_q.append(block_w_offset - (i*1000))

for i in blocks_for_q:
    arbitrum_maps.append(l2SubgraphHandler.paginate_results({}, orch_map_cb, l2SubgraphHandler.get_fee_reward, 100, {"block":i}))

fee_medians = []
reward_medians = []
fee_averages = []
reward_averages = []
for _map in arbitrum_maps:
    fee_shares = [float(val["feeShare"])/10000 for val in _map.values()]
    reward_cuts = [float(val["rewardCut"])/10000 for val in _map.values()]
    fee_medians.append(statistics.median(fee_shares))
    reward_medians.append(statistics.median(reward_cuts))
    fee_averages.append(statistics.mean(fee_shares))
    reward_averages.append(statistics.mean(reward_cuts))

data = {
    "fee_averages": fee_averages,
    "reward_averages": reward_averages,
    "fee_medians":fee_medians,
    "reward_medians": reward_medians
}
df = pd.DataFrame(data=data, index=blocks_for_q)

df.plot()
plt.show()


# diff_map = {}
# rolling_fee = {
#     "avg":0,
#     "min":0,
#     "max":0,
#     "no_change":0,
#     "cnt": 0
# }
# rolling_reward = {
#     "avg":0,
#      "min":0,
#     "max":0,
#     "no_change":0,
#     "cnt": 0
# }
# for l2_o in arbitrum_map.values():
#     if(l2_o["id"] in eth_mainnet_map if not sys.argv[1] else arbitrum_map.keys()):
#         l1_o = eth_mainnet_map[l2_o["id"]]
#         fee_diff = (float(l2_o["feeShare"]) - float(l1_o["feeShare"]))/10000
#         reward_diff = (float(l2_o["rewardCut"]) - float(l1_o["rewardCut"]))/10000


#         # calc new averages
#         if(fee_diff != 0):
#             rolling_fee["min"] = fee_diff if fee_diff < rolling_fee["min"] else rolling_fee["min"]
#             rolling_fee["max"] = fee_diff if fee_diff > rolling_fee["max"] else rolling_fee["max"]
#             rolling_fee["avg"] = (rolling_fee["cnt"] * rolling_fee["avg"] + fee_diff) / (rolling_fee["cnt"] + 1)
#         else:
#             rolling_fee["no_change"] = (rolling_fee["no_change"] + 1)
#         rolling_fee["cnt"] = (rolling_fee["cnt"] + 1)

#         if(reward_diff != 0):
#             rolling_reward["min"] = reward_diff if reward_diff < rolling_reward["min"] else rolling_reward["min"]
#             rolling_reward["max"] = reward_diff if reward_diff > rolling_reward["max"] else rolling_reward["max"]
#             rolling_reward["avg"] = (rolling_reward["cnt"] * rolling_reward["avg"] + reward_diff) / (rolling_reward["cnt"] + 1)
#         else:
#             rolling_reward["no_change"] = (rolling_reward["no_change"] + 1)
#         rolling_reward["cnt"] = (rolling_reward["cnt"] + 1)

#         diff_map[l2_o["id"]] = { fee_diff, reward_diff}

# print(
#     """
#     average fee share change: {fee_avg}
#     min fee share change: {fee_min}
#     max fee share change: {fee_max}
#     count of Os who changed fee share: {fee_changed}
#     count of Os who didn't change fee share: {fee_none}

#     average reward cut change: {reward_avg}
#     min reward cut change: {reward_min}
#     max reward cut change: {reward_max}
#     count of Os who changed fee share: {reward_changed}
#     count of Os who didn't change reward cut: {reward_none}
#     """.format(
#     fee_avg=rolling_fee["avg"], 
#     fee_min=rolling_fee["min"], 
#     fee_max=rolling_fee["max"], 
#     fee_none=rolling_fee["no_change"], 
#     fee_changed = rolling_fee["cnt"] - rolling_fee["no_change"],
#     reward_avg=rolling_reward["avg"], 
#     reward_min=rolling_reward["min"], 
#     reward_max=rolling_reward["max"], 
#     reward_none=rolling_reward["no_change"], 
#     reward_changed=rolling_reward["cnt"] - rolling_reward["no_change"]
# ))
