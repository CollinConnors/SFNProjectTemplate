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

#JWT
jwt = ""

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

class TestLogin:
    o=2
    @pytest.mark.run(order=o+1)
    def test_login_post(self):
        global jwt
        payload = {
            "username": "Username",
            "password": "Password"
        }
        res=requests.post(f'{backend_api}/login',json=payload,verify=False)
        assert(res.status_code==200)
        jwt = res.json().get('jwt',None)
        assert(not jwt==None)

    @pytest.mark.run(order=o+2)
    def test_hidden_get(self):
        global jwt
        headers = {"Authorization": f"Bearer {jwt}"}
        res=requests.get(f'{backend_api}/hidden', headers = headers, verify=False)
        assert(res.status_code==200)
        
        