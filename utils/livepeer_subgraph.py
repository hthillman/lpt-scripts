import requests

livepeer_subgraph_url = 'https://api.thegraph.com/subgraphs/name/livepeer/livepeer'

def paginate_results(acc_cb, query_cb, page_size):
    offset = 0
    _continue = True 
    acc = [0, 0]
    while _continue:
        cur = query_cb(offset, page_size)
        acc = acc_cb(acc, cur)
        if(len(cur)) < page_size:
            _continue = False
        else: 
            print("paginating ({offset})....".format(offset=offset))
        offset += page_size   
    return acc

def run_query(q):
    request = requests.post(livepeer_subgraph_url,
                            json={'query': q})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed - existing. Status {}. Query supplied: {}'.format(request.status_code, q))

def get_delegators(offset, page_size):
    result = run_query(_get_delegators_query(page_size, offset))
    return result["data"]["delegators"]

def _get_delegators_query(limit, skip):
    return "{ delegators(first: %s, skip: %s) { id } }" % (limit, skip)
