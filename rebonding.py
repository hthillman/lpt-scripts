from logging import exception
from utils.livepeer.subgraph import SubgraphQuery
import csv
import pandas as pd


page_size = 100

l2SubgraphHandler = SubgraphQuery()
l1SubgraphHandler = SubgraphQuery("mainnet")

filename = "rebonds.csv"


def rebond_acc_cb(acc, cur):
    _acc = acc
    for c in cur:
        round = c["round"]["id"]
        amt = float(c["amount"])
        if round in _acc.keys() and _acc[round]:
            _acc[round]["count"] += 1
            _acc[round]["amount"] += amt
            continue
        _acc[round] = { "count": 1, "amount": amt}
    return _acc

rebonds = l2SubgraphHandler.paginate_results({}, rebond_acc_cb, l2SubgraphHandler.get_recent_rebonds, page_size)
l1_rebonds = l1SubgraphHandler.paginate_results({}, rebond_acc_cb, l1SubgraphHandler.get_recent_rebonds_l1, page_size)

rebonds.update(l1_rebonds)

rounds = list(rebonds.keys())
count = []
amt = []
for round in rounds:
    count.append(rebonds[round]["count"])
    amt.append(rebonds[round]["amount"])

print(rounds)
_df = {"round": rounds, "moved_stake": count, "stake_amt": amt}

print(_df)
df = pd.DataFrame(_df)
df.sort_values(by="round").to_csv(r'rebonds.csv')

# with open(filename, 'w') as csvfile: 
#     # creating a csv writer object 
#     csvwriter = csv.DictWriter(csvfile, keys) 

#     # writing the data rows 
#     csvwriter.writerows(rebonds)