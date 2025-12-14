# yaml-language-server: $schema=https://learn.microsoft.com/schema/kernel-actions/kaschema.json
version: 1.0.0
name: local-ai-environment-setup-checklist
description: Setup and validation workflow for Aider, Ollama, Cursor IDE, Ngrok, and WSL2.

goals:
  - Detect what components are already installed to avoid duplicate installation
  - Install and configure Ollama inside WSL2
  - Install Aider and verify CLI functionality
  - Expose Ollama via Ngrok
  - Configure Cursor IDE to use the local Ollama model
  - Validate the entire environment end-to-end

steps:
  - id: precheck_ollama
    description: Check if Ollama is already installed
    command: which ollama

  - id: precheck_model
    description: Check if DeepSeek R1 model is already downloaded
    command: ollama list | grep deepseek-r1

  - id: precheck_ollama_running
    description: Check if Ollama is already running on port 11434
    command: netstat -tuln | grep 11434

  - id: precheck_aider
    description: Check if Aider is already installed
    command: which aider

  - id: precheck_ngrok
    description: Check if Ngrok is installed on Windows host
    manual: true

  - id: precheck_cursor_config
    description: Check if Cursor already has a custom model configured
    manual: true

  - id: install_ollama
    description: Install Ollama in WSL2 using official script
    command: curl -fsSL https://ollama.ai/install.sh | sh

  - id: pull_model
    description: Pull DeepSeek R1 model for Ollama
    command: ollama pull deepseek-r1

  - id: set_network_vars
    description: Configure Ollama environment variables for external access
    command: |
      export OLLAMA_HOST=0.0.0.0:11434
      export OLLAMA_ORIGINS="*"

  - id: start_ollama
    description: Start Ollama server in background
    command: ollama serve &

  - id: install_aider
    description: Install Aider CLI
    command: pip install aider-chat

  - id: ngrok_auth
    description: Authenticate Ngrok with the provided token
    command: ngrok authtoken $NGROK_AUTH_TOKEN

  - id: ngrok_tunnel
    description: Create Ngrok tunnel mapping to WSL port 11434
    command: ngrok http 11434 --host-header="localhost:11434"

  - id: cursor_disable_defaults
    description: Disable default cloud models in Cursor IDE
    manual: true

  - id: cursor_add_model
    description: Add a new model entry in Cursor IDE
    manual: true

  - id: cursor_model_name
    description: Set Cursor model name to deepseek-r1:latest
    manual: true

  - id: cursor_base_url
    description: Configure Cursor to override base OpenAI URL with Ngrok URL + /v1
    manual: true

  - id: cursor_api_key
    description: Add placeholder API key (non-empty)
    manual: true

validation:
  - id: validate_ollama_install
    description: Confirm Ollama binary exists
    command: which ollama

  - id: validate_model_download
    description: Confirm DeepSeek R1 model is installed
    command: ollama list | grep deepseek-r1

  - id: validate_ollama_listening
    description: Confirm Ollama is actively listening on 0.0.0.0:11434
    command: netstat -tuln | grep 11434

  - id: validate_aider_install
    description: Confirm Aider binary exists
    command: which aider

  - id: validate_aider_run
    description: Confirm Aider launches with the Ollama model
    command: aider --model ollama_chat/deepseek-r1 --yes

  - id: validate_ngrok
    description: Validate Ngrok tunnel availability
    command: curl -I $NGROK_URL

  - id: validate_cursor_output
    description: Verify Cursor AI Fixup/Chat works with local model
    manual: true
```

## more context version

```md
Setup Guide: Aider, Ollama, and Cursor in WSL 2
This guide provides a structured plan for running Aider with Ollama locally for free within the Cursor IDE environment using WSL 2 and Ngrok for connectivity.

Implementation Plan
Follow these steps in order to set up your local AI environment. Complete all items in this section before moving to the Validation section.
	•	Install Ollama in WSL 2: Open your Ubuntu WSL terminal and run the official install script: curl -fsSL ollama.ai | sh
	•	Pull a Model: Download a compatible model (e.g., DeepSeek R1) inside WSL: ollama pull deepseek-r1
	•	Configure Network Access: In the WSL terminal session you plan to run Ollama from, set environment variables to allow external connections: export OLLAMA_HOST=0.0.0.0:11434 and export OLLAMA_ORIGINS="*"
	•	Start Ollama Server: Launch the Ollama service in the background within WSL: ollama serve &
	•	Install Aider in WSL: Use pip to install the Aider CLI tool: pip install aider-chat
	•	Set Up Ngrok: Install Ngrok on your Windows host system (download from the official Ngrok website) and authenticate your account token using ngrok authtoken <your_token>
	•	Create Ngrok Tunnel: In a Windows Command Prompt or PowerShell, create a tunnel to the WSL Ollama port: ngrok http 11434 --host-header="localhost:11434"
	•	Configure Cursor IDE - Disable Defaults:Open Cursor IDE, navigate to Settings -> AI, and disable any default cloud models (e.g., GPT-4).
	•	Configure Cursor IDE - Add Model: In the Cursor AI Settings, click the "Add Model" button.
	•	Configure Cursor IDE - Define Model Name:Set the "Model Name" field to exactly match your local model name: deepseek-r1:latest
	•	Configure Cursor IDE - Override Base URL:Enable "Override OpenAI Base URL" and paste the HTTPS forwarding URL from your Ngrok terminal output, adding /v1 to the end (e.g., xxxx.ngrok-free.app).
	•	Configure Cursor IDE - Add Placeholder API Key: Add a non-empty placeholder value (e.g., ollama) into the "API Key" field to satisfy the UI requirements.

Validation Checklist
Verify each component works correctly using these tests.
	•	Verify Ollama Installation: Run which ollama in WSL and confirm a valid path is returned (e.g., /usr/local/bin/ollama).
	•	Verify Model Download: Run ollama list in WSL and confirm deepseek-r1 (or chosen model) appears in the list.
	•	Verify Ollama Service is Listening: Run netstat -tuln in WSL and confirm a process is listening on 0.0.0.0:11434.
	•	Verify Aider Installation: Run which aiderin WSL and confirm a valid path is returned (e.g., /usr/bin/python3-aider).
	•	Test Aider Functionality: Run aider --model ollama_chat/deepseek-r1 in a project directory in WSL and ensure it launches a working chat session.
	•	Verify Ngrok Tunnel Status: Check the Ngrok terminal output. The "Status" line should read "online" and provide an active HTTPS URL.
	•	Final System Test in Cursor: Open a code file in Cursor, highlight some code, and use the "AI Fixup" or Chat feature. The local model should process the request and generate a correct response/code modification.
```
