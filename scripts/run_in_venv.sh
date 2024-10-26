#!/bin/bash
python3.12 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 gui.py
deactivate
