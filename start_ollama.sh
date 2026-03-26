#!/bin/bash
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export OLLAMA_MODELS="$PROJECT_DIR/ollama_data"
export OLLAMA_HOST="127.0.0.1:11434"

echo "🚀 Запуск локальной Ollama"
echo "Данные: $OLLAMA_MODELS"
echo "URL: http://$OLLAMA_HOST"
echo ""

"$PROJECT_DIR/ollama_local/ollama" serve
