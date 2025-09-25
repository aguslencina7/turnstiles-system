# Project Structure (Turnstile System)

This document serves as a reference of the folder and file organization for the project.

molinete-system/
│
├── hardware/               # Direct control of GPIOs (inputs/outputs)
│ ├── init.py
│ ├── gpio_controller.py    # Class for handling GPIOs (simulate buttons, read and confirmation)
│ ├── relay_driver.py       # Functions to drive relays
│ ├── sensors.py            # Reading of passage confirmation, emergency, etc.
│
├── core/                   # Business logic (state machine)
│ ├── init.py
│ ├── state_machine.py      # Cycle IDLE → enable → confirm → log
│ ├── access_control.py     # User credential validation (RFID, PIN, API)
│ ├── config.py             # General configuration (timers, modes S1, NA/NC)
│
├── data/                   # Database and persistence
│ ├── init.py
│ ├── database.py           # SQLite/Postgres connection
│ ├── models.py             # Tables definition (users, access logs, turnstiles)
│
├── api/                    # External interfaces
│ ├── init.py
│ ├── rest_api.py           # REST endpoints (Flask or FastAPI)
│ ├── mqtt_client.py        # Optional: IoT style communication
│
├── ui/                     # Administration interface
│ ├── init.py
│ ├── web_app.py            # Web panel (Flask/Django)
│ ├── templates/            # HTML
│ └── static/               # CSS, JS
│
├── tests/                  # Tests
│ ├── test_gpio.py
│ ├── test_state_machine.py
│ ├── test_database.py
│
├── utils/                  # Helper functions
│ ├── init.py
│ ├── logger.py             # Logging handler
│ ├── helpers.py            # General utilities
│
├── main.py                 # System entry point
├── requirements.txt        # Python dependencies
├── PROJECT-STRUCTURE.md    # Project structe
└── README.md               # Project overview