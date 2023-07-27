import json

def Response(data):
    with open('routers/constants/http_status_codes.json') as f:
        dic = json.load(f)
        return dic[data]

