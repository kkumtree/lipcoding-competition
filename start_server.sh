#!/bin/bash
cd /Users/kkumtree/github/lipcoding-competition
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
