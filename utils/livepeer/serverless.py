import requests

serverless_root = 'https://leaderboard-serverless.vercel.app/api'

def is_high_performing_orchestrator(address):
    res = requests.get('{0}/aggregated_stats?orchestrator={1}'.format(serverless_root, address))
    res_json = res.json()
    if not address in res_json.keys():
        return False
    keys = res_json[address].keys()
    _max = 0
    for k in keys:
        if(res_json[address][k]["score"] > _max):
            _max = res_json[address][k]["score"]
    return _max >= 0.63
