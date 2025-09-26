from utils.loggers import logger
from core.state_machine import TurnstileStateMachine

def main():
    logger.info("Turnstile system initialized (setup mode)")
    print("OK: enviroment ready.")

    sm = TurnstileStateMachine()
    print("Turnstile system (simulated). Write credentials or 'q' for exit.")

    while True:
        raw = input(">> Credential: ")
        if raw.lower() == "q":
            break
        result = sm.process_credential(raw)
        print(f"Result: {result}")


if __name__ == "__main__":
    main()