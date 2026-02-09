#!/bin/bash
# Script to run the backend server
echo "Starting OrbitThink Backend..."
uvicorn backend.main:app --reload --port 8000
