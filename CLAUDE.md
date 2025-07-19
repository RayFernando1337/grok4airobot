# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based AI voice assistant project that creates "Bot-tholomew" - a conversational AI companion. The project uses Pipecat framework to build a real-time voice pipeline integrating speech-to-text, LLM processing, and text-to-speech.

## Architecture

The codebase consists of:
- `main.py`: Core pipeline implementation using Pipecat framework
- `v1.txt`, `v2.txt`, `v3.txt`: Bot-tholomew personality configuration files (prompts)

### Key Components

1. **Audio I/O**: LocalAudioTransport for microphone/speaker access
2. **Speech-to-Text**: AssemblyAI STT Service with voice activity detection
3. **LLM**: Grok-4 model via OpenRouter API
4. **Text-to-Speech**: ElevenLabs streaming TTS with low-latency mode

## Development Commands

### Environment Setup
This project uses the `grokaibot` conda environment. 

**For Cursor IDE:**
1. Open Command Palette (`Cmd + Shift + P`)
2. Select "Python: Select Interpreter"  
3. Choose: `/Users/ray/miniforge3/envs/grokaibot/bin/python`
4. The `.vscode/settings.json` file configures the environment automatically

**For Terminal:**
```bash
conda activate grokaibot
```

### Running the Application
Due to a known issue with Claude Code and conda environment activation, use the full Python path:
```bash
/Users/ray/miniforge3/envs/grokaibot/bin/python main.py
```
Use Ctrl-C to stop the application.

**Note**: The conda environment contains both `pipecat` (units library) and `pipecat-ai` (AI framework). The AI framework is accessed through `pipecat.*` imports but requires the correct Python environment.

### Environment Variables Required
- `ASSEMBLYAI_API_KEY`: For speech-to-text service
- `OPENROUTER_API_KEY`: For Grok-4 LLM access
- `ELEVENLABS_API_KEY`: For text-to-speech service

### Dependencies
The project uses the Pipecat framework. Install dependencies with:
```bash
pip install pipecat-ai
```

## Code Patterns

- The pipeline pattern chains audio input → STT → LLM → TTS → audio output
- Services are configured with API keys from environment variables
- The bot's personality is defined in separate text files (v1.txt, v2.txt, v3.txt)
- Uses 16kHz sample rate for audio processing

## Important Notes

- OpenRouter requires a Referer header for API requests (configured in main.py:26)
- The project uses Grok-4 model specifically (x-ai/grok-4)
- Voice activity detection can be configured as 'strict', 'default', or 'loose'
- ElevenLabs voice is set to "nova" by default