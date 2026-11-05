#!/bin/bash
echo 'Creating isolated virtual environment (.venv)...'
python3 -m venv .venv
echo 'Installing required packages...'
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt
echo 'Setup complete!'
