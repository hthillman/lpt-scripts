from logging import exception
from utils.livepeer.subgraph import SubgraphQuery
from utils.livepeer.serverless import high_performing_orchestrators

page_size = 100

l2SubgraphHandler = SubgraphQuery()
l1SubgraphHandler = SubgraphQuery("mainnet")

high_performing = high_performing_orchestrators()

def nonmigrated_orch_acc_cb(acc, cur):
    _acc = acc
    for c in cur:
     if(c["active"] and c["id"] not in migrated["orchestrators"]["addresses"]):
        _acc["addresses"].append(c["id"])
        _acc["total_stake"] += float(c["totalStake"])
        if(c["id"] in high_performing.keys() and high_performing[c["id"]]):
            _acc["high_performing"].append(c["id"])
    return _acc


def migrator_acc_cb(acc, cur):
    _acc = acc
    for c in cur:
        if(c["l1Addr"] == c["delegate"]):
            _acc["orchestrators"]["addresses"].append(c["l1Addr"])
            _acc["orchestrators"]["total_stake"] += float(c["delegatedStake"])
            _acc["orchestrators"]["total_stake"] += float(c["stake"])
            if(c["l1Addr"] in high_performing.keys() and high_performing[c["l1Addr"]]):
                _acc["orchestrators"]["high_performing"].append(c["l1Addr"])
        elif(c["l1Addr"] != c["delegate"]):
            _acc["delegators"]["addresses"].append(c["l1Addr"])
            _acc["delegators"]["total_stake"] += float(c["delegatedStake"])
    return _acc

def delegator_claim_cb(acc, cur):
    _acc = acc
    for c in cur:
        _acc["delegators"]["claimed_stake"].append(c["delegator"])
    return _acc

# field names
migrator_initial_acc = {
    "orchestrators": {
        "addresses": [],
        "total_stake": 0,
        "high_performing":[]
    },
    "delegators": {
        "addresses": [],
        "total_stake": 0,
        "claimed_stake":[]
    }
}
nonmigrated_orch_initial_acc = {
 "addresses": [],
 "total_stake": 0,
 "high_performing": []
}

claimed_stake = l2SubgraphHandler.paginate_results(
    migrator_initial_acc, delegator_claim_cb, l2SubgraphHandler.get_delegator_claim, page_size)
migrated = l2SubgraphHandler.paginate_results(
    migrator_initial_acc, migrator_acc_cb, l2SubgraphHandler.get_migrators, page_size)
nonmigrated = l1SubgraphHandler.paginate_results(
    nonmigrated_orch_initial_acc, nonmigrated_orch_acc_cb, l1SubgraphHandler.get_orchestrators, page_size)


print(
    """
    ORCHESTRATORS 

    Migrated: {migratedCount}
    Migrated Stake: {migratedStake}
    High-performing migrated: {highPerformingMigrated}

    Did not migrate: {nonMigratedCount}
    Did not migrate Stake: {nonMigratedStake}
    High-performing did not migrate: {highPerformingNonMigrated}
    """.format(migratedCount=len(migrated["orchestrators"]["addresses"]), migratedStake=migrated["orchestrators"]["total_stake"],
    highPerformingMigrated=len(migrated["orchestrators"]["high_performing"]),
    nonMigratedCount=len(nonmigrated["addresses"]), nonMigratedStake=nonmigrated["total_stake"],
    highPerformingNonMigrated=len(nonmigrated["high_performing"])
    )
)

print(
    """
    DELEGATORS 

    Claimed Stake: {claimedStake}

    Delegator's Orchestrator did not migrate: {nonMigratedCount}
    """.format(migratedCount=len(migrated["delegators"]["addresses"]), claimedStake=len(migrated["delegators"]["claimed_stake"]),
    nonMigratedCount=len(nonmigrated["addresses"])
    )
)
