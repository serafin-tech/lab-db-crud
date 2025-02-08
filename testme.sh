#!/bin/bash

source venv/bin/activate

export PYTHONPATH=$PYTHONPATH:.

pytest tests/ \
    --cov=crud_app \
    --cov-report=html:coverage_report.html \
    --cov-report=term
