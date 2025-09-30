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
- Python 3.10+'
- For Raspberry PI also install evdev, RPi.GPIO, gpiozero
- See `requirements.txt` for dependencies.

## Installation
```bash
git clone https://github.com/yourname/turnstile-system.git
cd turnstile-system
pip install -r requirements.txt

## Dev (PC)
pip install -r requirements.txt
cp .env.example .env.dev   # completar valores
cp .env.dev .env
python main_pc.py

## Raspberry (cuando toque)
pip install -r requirements.txt
pip install evdev RPi.GPIO gpiozero
cp .env.example .env.prod  # completar reales
cp .env.prod .env
python main_pi.py
