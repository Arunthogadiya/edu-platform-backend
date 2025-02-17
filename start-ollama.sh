#!/bin/bash


docker pull ollama/ollama:latest

docker stop ollama

docker rm ollama

docker run --restart unless-stopped --gpus '"device=0"' \
	-v `pwd`/models:/root/.ollama -p 11437:11434 --name ollama-genai \
	-e OLLAMA_MAX_LOADED_MODELS=1 \
	-e OLLAMA_NUM_PARALLEL=1 \
	-e OLLAMA_MAX_QUEUE=3 \
	-e OLLAMA_KEEP_ALIVE=-1 \
	-e OLLAMA_DEBUG=1 \
	-e OLLAMA_FLASH_ATTENTION=1 \
	-d ollama/ollama:latest

echo "OLLama server running on 11437 port"