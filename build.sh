#!/bin/bash

# Install distutils manually
apt-get update && apt-get install -y python3-distutils

# Create venv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the app
python app.py  # or whatever your entry point is
