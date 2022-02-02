from utils.livepeer.subgraph import get_orchestrators, paginate_results

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

res = paginate_results(initial_acc,acc_cb, get_orchestrators, page_size)


print(
    """
    Active: {active}

    Inactive: {inactive}

    """.format(active=res[0], inactive=res[1])
)