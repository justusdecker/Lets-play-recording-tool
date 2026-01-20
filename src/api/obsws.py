import json
import hashlib
import base64
import websocket

class OBSWSClient:
    """
    By using OBS v5 we get the current recording time etc.
    """
    def __init__(self, host="localhost", port=4455, password=""):
        self.url = f"ws://{host}:{port}"
        self.password = password
        self.ws = None
        self.msg_id = 0
    
    def __generate_auth(self, salt, challenge) -> str:
        # hash & salt
        secret_hash = hashlib.sha256((self.password + salt).encode('utf-8')).digest()
        secret_b64 = base64.b64encode(secret_hash).decode('utf-8')
        
        # Hash the result with the challenge
        auth_hash = hashlib.sha256((secret_b64 + challenge).encode('utf-8')).digest()
        auth_b64 = base64.b64encode(auth_hash).decode('utf-8')
        return auth_b64

    def connect(self)  -> str | None:
        """
        Connects to OBSWS, if any error is raised during this: we return a string(containing the Exception) else None
        """
        try:
            self.ws = websocket.create_connection(self.url)
            
            # Get hello
            
            hello = json.loads(self.ws.recv())
            print("Connection to OBS established!")
            # generate identify
            
            identify_data = {
                "op": 1, # OpCode 1: Identify
                "d": {"rpcVersion": 1,}
            }
            # send identify
            if "authentication" in hello["d"]:
                salt = hello["d"]["authentication"]["salt"]
                challenge = hello["d"]["authentication"]["challenge"]
                auth_string = self.__generate_auth(salt, challenge)
                
                identify_data["d"]["authentication"] = auth_string

            self.ws.send(json.dumps(identify_data))
            
            identified = json.loads(self.ws.recv())
            if identified["op"] == 2:
                print("Auth Success!")
        except Exception as E:
            return str(E)
        
    def call(self, request_type, request_data=None):
        """
        Sends a call / a manually Request(OpCode 6) to the WS
        """
        try:
            self.msg_id += 1
            payload = {
                "op": 6, # OpCode 6: Request
                "d": {
                    "requestType": request_type,
                    "requestId": f"req_{self.msg_id}",
                    "requestData": request_data or {}
                }
            }
            
            self.ws.send(json.dumps(payload))
            return json.loads(self.ws.recv())
        except Exception as E:
            return {'error': str(E)}

# --- How to work with ---
if __name__ == "__main__":
    obs = OBSWSClient(password="")
    try:
        obs.connect()
        
        
        response = obs.call("GetOutputStatus",{"outputName": 'adv_file_output'})
        print(response['d']['responseData']['outputTimecode'])
    finally:
        if obs.ws:
            obs.ws.close()