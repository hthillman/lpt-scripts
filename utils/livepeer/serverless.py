import requests

serverless_root = 'https://leaderboard-serverless.vercel.app/api'


def high_performing_orchestrators():
    res = requests.get('{0}/aggregated_stats'.format(serverless_root))
    res_json = res.json()
    orch_high_performing_status = {}
    keys = res_json.keys()
    for k in keys:
        _max = 0
        for j in res_json[k]:
            if(res_json[k][j]["score"] > _max):
                _max = res_json[k][j]["score"]
        orch_high_performing_status[k] = _max >= 0.63
    return orch_high_performing_status
