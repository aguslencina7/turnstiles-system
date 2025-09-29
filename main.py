from utils.loggers import logger
from core.state_machine import TurnstileStateMachine
from api.rest_api import ApiClient
from hardware.gpio_controller import GpioSim
from hardware.credential_reader import CredentialReader

def main():
    logger.info("Turnstile system initialized (setup mode)")
    print("OK: enviroment ready.")

    #Config
    api = ApiClient(simulated=True)
    gpio = GpioSim()
    reader = CredentialReader()

    #State machine
    sm = TurnstileStateMachine(api=api, gpio=gpio, config={"GATE_ID": "turnstile_01"})
    print("Turnstile system (simulated). Write credentials or 'q' for exit.")

    #Main loop
    while True:
        raw = input(">> Credential: ")
        if raw.lower() == "q":
            break
        result = sm.process_credential(raw)
        print(f"Result: {result}")


if __name__ == "__main__":
    main()