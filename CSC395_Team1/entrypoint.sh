#!/bin/bash

ollama serve &

until curl -s http://localhost:11434; do
    echo "Waiting for Ollama to start..."
    sleep 5
done

ollama pull orca-mini:3b-q4_1

wait
