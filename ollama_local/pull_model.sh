#!/bin/bash
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export OLLAMA_HOST="http://127.0.0.1:11434"

echo "📥 Загрузка модели llama3.2..."
"$PROJECT_DIR/ollama_local/ollama" pull llama3.2
