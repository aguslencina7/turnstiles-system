#get_token()

#validate_credentials(credential, gate_id, token) 
# returns {authorized, user_id}

#timeouts, backoff retrys, error handle (4xx, 5xx)

#simulate response for testing

import time

class ApiClient:
    def __init__(self, simulated: bool = True):
        self.simulated = simulated
    
    def get_token(self) -> str:
        return "SIM_TOKEN" if self.simulated else NotImplemented # Later real OAuath2
    
    def validate_credential(self, credential: str, gate_id: str, token: str) -> dict:
        if self.simulated:
            time.sleep(0.1)
            allow = credential[-1] in "02468" #Simulates if credential ends in one of the numbers of the list to allow access
            return {"authorized": allow, "user_id": f"user_{credential[-4:]}"} 
        raise NotImplementedError   

        resp = requests.post(
            f"{self.base_url}/validate",
            headers = {"Authorization": f"Bearer {token}"},
            json = {"credential": credential, "gate_id": gate_id},
            timeout = 3
        )

    