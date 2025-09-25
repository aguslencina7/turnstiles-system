# Turnstile System (Molinete)

This project is a Raspberry Pi based access control system for turnstiles.
It connects to the CAM-1 controller to manage entry/exit and logs every event.

## Features
- GPIO control of relays to unlock turnstiles (CW/CCW).
- Reads passage confirmation from CAM-1.
- Local database for users and events (SQLite/Postgres).
- Web interface for administration.
- REST API for integration with external systems.

## Requirements
- Raspberry Pi (tested on Pi 4).
- Python 3.10+
- See `requirements.txt` for dependencies.

## Installation
```bash
git clone https://github.com/yourname/turnstile-system.git
cd turnstile-system
pip install -r requirements.txt
