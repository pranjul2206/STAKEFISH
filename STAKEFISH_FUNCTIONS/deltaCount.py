import requests

def getData():
    GET_URL = 'http://localhost:5000/getdelta'
    ret = requests.get(GET_URL).json()
    return ret['count']

print('Number of time the gap was greater than 2 hours is ',getData())
