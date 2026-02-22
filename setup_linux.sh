#!/bin/bash

echo "================================"
echo "  AI-MOZG AUTO SETUP"
echo "================================"
echo ""

echo "1. Obnovlenie sistemy..."
sudo apt update && sudo apt upgrade -y

echo ""
echo "2. Ustanovka Python i pip..."
sudo apt install python3 python3-pip python3-venv -y

echo ""
echo "3. Ustanovka zavisimostey proekta..."
pip3 install -r requirements.txt

echo ""
echo "4. Ustanovka Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo ""
echo "5. Zapusk Ollama servera..."
ollama serve &
sleep 5

echo ""
echo "6. Zagruzka modeli llama3.2..."
ollama pull llama3.2

echo ""
echo "================================"
echo "  USTANOVKA ZAVERSHENA!"
echo "================================"
echo ""
echo "Zapusti AI-mozg:"
echo "  python3 ai_brain.py"
echo ""
