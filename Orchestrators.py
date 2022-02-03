from utils.livepeer.subgraph import SubgraphQuery

page_size = 100

def acc_cb(acc, cur):
    _acc = acc
    for c in cur:
     if(c["active"]):
        _acc[0] += 1
     else: 
        _acc[1] += 1
    return _acc

# field names 
initial_acc = [0,0]

subgraphHandler = SubgraphQuery()
res = subgraphHandler.paginate_results(initial_acc,acc_cb, subgraphHandler.get_orchestrators, page_size)


print(
    """
    Active: {active}

    Inactive: {inactive}

    """.format(active=res[0], inactive=res[1])
)