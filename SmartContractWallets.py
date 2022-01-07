from web3 import Web3 
from utils.eth import get_web3_client, checksum_list
from utils.livepeer.subgraph import get_delegators, paginate_results

w3 = get_web3_client()


page_size = 100

known_livepeer_wallets = checksum_list(['0xBBB3c3f5Fee342431285D9dac658f5D3b8830A7A',
'0x611e622605AF99D0Adc545F5783Cb77d37489639', 
'0xdFdba7BeAF641CD34Dd4d30834afA1CB3fA73544',
'0x2ABA7Cb4B2eBA506E404715234aC7Ac1b0948dB9',
'0xb10A00cb31cBA60b5879b9Cc55858F5692731bF7',
'0xB14Cf249E7cBcAc99A28e7fF2972f9167af20c9B',
'0x08D185fF976a5aEf915689316e5b2850A85AC3F2',
'0xBB0A9EaC8366e9766885B8CB5F92321f85316b39',
'0x5BDb62B4a0C784B29fBB317dEd90CfEFfC9312f2',
'0x94be254189EEa0878a773BE736f1D88135732EB2',
'0x94320EBA1E8eec8a218845279e7d8CF93D6c2EC9',
'0xD1b59DAdfd9F4B81768Aed17bEeEb3C351D83822',
'0x6f041f39dd22844c64354cAD1B6F1b9aA157221D',
'0x5F80Aa384133588E927cA588Acc44e7C65C2D565',
'0xb84550d8edd88F4916301017dF79002D6c58dAa6',
'0xD9CfeB316F2129249CCe3752294FE71d46336E05',
'0xc86bd100eDaea721F9Cd1A095B59B5d14eB56C2D',
'0x5f4DDe2AB0C5C338b67c271Bc9a52b99BEc5884d'])

def acc_cb(acc, cur):
    _acc = acc
    for c in cur:
        _address = Web3.toChecksumAddress(c['id'])
        if(_address not in known_livepeer_wallets):
            code = w3.eth.get_code(_address)
            print("code", code, bool(code))
            if(code):
                _acc[0] += 1
                _acc[2].append(_address)
            else:
                _acc[1] += 1
    return _acc

initial_acc = [0, 0, []]
wallets = paginate_results(initial_acc, acc_cb, get_delegators, page_size)



print(
    """
    Contract wallets: {contract}
    Noncontract wallets: {noncontract}
    Contract wallet addresses: {addresses}
    """.format(contract=wallets[0], noncontract=wallets[1], addresses=wallets[2])
)

