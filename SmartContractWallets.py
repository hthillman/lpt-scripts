from web3 import Web3 
from utils.eth import get_web3_client
from utils.livepeer_subgraph import get_delegators, paginate_results

w3 = get_web3_client()


page_size = 100

def acc_cb(acc, cur):
    count = acc
    for c in cur:
        code = w3.eth.get_code(Web3.toChecksumAddress(c['id']))
        if(code):
            count[0] += 1
        else:
            count[1] += 1
    return count


wallets = paginate_results(acc_cb, get_delegators, page_size)
print(wallets)

print(
    """
    Contract wallets: {contract}
    Noncontract wallets: {noncontract}
    """.format(contract=wallets[0], noncontract=wallets[1])
)