from utils.loggers import logger

import time

class ApiClient:
    def __init__(self, simulated: bool = True):
        self.simulated = simulated
    
    def get_token(self) -> str:
        if self.simulated:
            return "SIM_TOKEN"
        else:
            return NotImplemented
        # Later real OAuath2
    
    def validate_credential(self, credential: str, gate_id: str, token: str) -> dict:
        if self.simulated:
            time.sleep(0.1)
            allow = credential[-1] in "02468" # Dummy rule
            logger.info(f"Credential state: {allow}, user_id: user_{credential[-4:]}")
            return {"authorized": allow, "user_id": f"user_{credential[-4:]}"} 
        raise NotImplementedError   

        resp = requests.post(
            f"{self.base_url}/validate",
            headers = {"Authorization": f"Bearer {token}"},
            json = {"credential": credential, "gate_id": gate_id},
            timeout = 3
        )

    