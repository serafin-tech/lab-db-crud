#!/bin/bash

source venv/bin/activate

PYTHONPATH=$PYTHONPATH:. python3.12 crud_app/app.py
