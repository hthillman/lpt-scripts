from utils.livepeer.subgraph import SubgraphQuery

page_size = 100

def orch_acc_cb(acc, cur):
    _acc = acc
    for c in cur:
     if(c["active"] and c["id"] in migrated):
        _acc[0] += 1
     else: 
        _acc[1] += 1
    return _acc

def migrator_acc_cb(acc, cur):
    _acc = acc
    for c in cur:
        if(c["l1Addr"]):
            _acc.append(c["l1Addr"])
    return _acc

# field names 
migrator_initial_acc = []
orch_initial_acc = [0,0]

subgraphHandler = SubgraphQuery(True)

print(subgraphHandler.livepeer_subgraph_url)

migrated = subgraphHandler.paginate_results(migrator_initial_acc,migrator_acc_cb, subgraphHandler.get_migrators, page_size)
res = subgraphHandler.paginate_results(orch_initial_acc,orch_acc_cb, subgraphHandler.get_orchestrators, page_size)


print(
    """
    ORCHESTRATORS 

    Migrated: {migrated}

    Did not migrate: {nonmigrated}

    """.format(migrated=res[0], nonmigrated=res[1])
)