from logging import exception
from utils.livepeer.subgraph import SubgraphQuery

page_size = 100

l2SubgraphHandler = SubgraphQuery("arbitrum-rinkeby")
l1SubgraphHandler = SubgraphQuery("rinkeby")

def nonmigrated_orch_acc_cb(acc, cur):
    _acc = acc
    for c in cur:
     if(c["active"] and c["id"] not in migrated["orchestrators"]["addresses"]):
        _acc["addresses"].append(c["id"])
        _acc["total_stake"] += float(c["totalStake"])
    return _acc


def migrator_acc_cb(acc, cur):
    _acc = acc
    for c in cur:
        if(c["l1Addr"] == c["delegate"]):
            _acc["orchestrators"]["addresses"].append(c["l1Addr"])
            _acc["orchestrators"]["total_stake"] += float(c["delegatedStake"])
            _acc["orchestrators"]["total_stake"] += float(c["stake"])
        elif(c["l1Addr"] != c["delegate"]):
            _acc["delegators"]["addresses"].append(c["l1Addr"])
            _acc["delegators"]["total_stake"] += float(c["delegatedStake"])
    return _acc


# field names
migrator_initial_acc = {
    "orchestrators": {
        "addresses": [],
        "total_stake": 0
    },
    "delegators": {
        "addresses": [],
        "total_stake": 0
    }
}
nonmigrated_orch_initial_acc = {
 "addresses": [],
 "total_stake": 0
}

migrated = l2SubgraphHandler.paginate_results(
    migrator_initial_acc, migrator_acc_cb, l2SubgraphHandler.get_migrators, page_size)
nonmigrated = l1SubgraphHandler.paginate_results(
    nonmigrated_orch_initial_acc, nonmigrated_orch_acc_cb, l1SubgraphHandler.get_orchestrators, page_size)


print(
    """
    ORCHESTRATORS 

    Migrated: {migratedCount}
    Migrated Stake: {migratedStake}

    Did not migrate: {nonMigratedCount}
    Did not migrate Stake: {nonMigratedStake}
    """.format(migratedCount=len(migrated["orchestrators"]["addresses"]), migratedStake=migrated["orchestrators"]["total_stake"],
    nonMigratedCount=len(nonmigrated["addresses"]), nonMigratedStake=nonmigrated["total_stake"]
    )
)
