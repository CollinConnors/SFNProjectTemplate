import pytest
import requests
import json

#Server Settings
protocol= 'http'
ip='localhost'
baseurl='api/v1'
headers = {"Content-Type": "application/json"}

#Servers
backend_api = f'{protocol}://{ip}/{baseurl}'

class TestAlive:
    o=0
    @pytest.mark.run(order=o+1)
    def test_backend_api_get(self):
        res=requests.get(f'{backend_api}/',verify=False)
        assert(res.status_code==200)
        j=json.loads(res.text)
        assert(j=={'alive':True})

    @pytest.mark.run(order=o+2)
    def test_backend_api_post(self):
        res=requests.post(f'{backend_api}/',json={'alive':True},verify=False)
        assert(res.status_code==200)
        j=json.loads(res.text)
        assert(j=={'alive':True})