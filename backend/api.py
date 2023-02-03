"""The backend API for the MintBlockchain Applictaion

This modules uses Falcon
"""

#---------------IMPORT-----------------
#Base Libs

import sys #For Debugging
import traceback #For Debugging

#Installed Libs
import falcon.asgi

#Set API Configurations
app = falcon.asgi.App(cors_enable=True)
base_url="/api/v1"
responseHeaders = {'Access-Control-Allow-Origin': '*'}
debug = True

#--------------API ENDPOINTS-----------------
#Endpoint URL = {base_url}/
class TestEndpoint:
    """Test if the server is alive
    
        Endpoint:
            {base_url}/

        Methods:
            GET, POST
    """
    async def on_get(self, req, resp):
        """Test if the server responds to GET requests
        
        | Endpoint: GET {base_url}/
        |
        | Responce:
        |   200:    
        |       {alive : True}
        |
        | Example Request:
        |   curl --request GET --url http://localhost:443/api/v1/
        |
        | Exampe Responce: 
        |    {
        |       "alive" : true
        |    }
        """
        resp.set_headers(responseHeaders)
        resp.media = {'alive':True}
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp):
        """Test if the server responds to POST requests

        | Endpoint: POST {base_url}/
        |
        | Args:
        |     Arbitrary JSON
        | 
        | Responce:
        |   200:    
        |       Same JSON data sent by the user
        |
        | Example Request:
        |   curl --request POST --url http://localhost:443/api/v1/ --header 'Content-Type: application/json' --data '{"test":"test"}'
        |
        | Exampe Responce: 
        |    {
        |       "test" : "test"
        |    }
        """
        try:
            raw_data = await req.media
            resp.set_headers(responseHeaders)
            resp.media = raw_data
            resp.status = falcon.HTTP_200
        except Exception as e: #Use for debugging
            if debug:
                tb = sys.exc_info()[-1]
                print(f'ERROR:\tLine {traceback.extract_tb(tb, limit=1)[-1][1]} ---- {e}')
            resp.set_headers(responseHeaders)
            resp.media = {'ERROR':'Error on Test Endpoint'}
            resp.status = falcon.HTTP_404

#--------------ASSIGN ENDPOINTS--------------------
test_endpoint=TestEndpoint()
"""{base_url}/"""

#--------------ASSIGN Routes--------------------
app.add_route(f'{base_url}/', test_endpoint)