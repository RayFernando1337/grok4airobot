import asyncio
import os
import sys
from loguru import logger

from pipecat.frames.frames import EndFrame, LLMMessagesFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_response import (
    LLMAssistantResponseAggregator, LLMUserResponseAggregator
)
from pipecat.transports.base_output import TransportParams
from pipecat.vad.silero import SileroVADAnalyzer
from pipecat.transports.local.audio import LocalAudioTransport
from pipecat.services.assemblyai import AssemblyAISTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.elevenlabs import ElevenLabsTTSService

# Configure logging
logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

# Load Bot-tholomew's personality
try:
    with open("v1.txt", "r") as f:
        system_prompt = f.read().strip()
except FileNotFoundError:
    system_prompt = "You are Bot-tholomew, a helpful robot assistant."


async def main():
    # Initialize transport with VAD
    transport = LocalAudioTransport(
        TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
            vad_audio_passthrough=True
        )
    )
    
    # Initialize STT service
    stt = AssemblyAISTTService(
        api_key=os.getenv("ASSEMBLYAI_API_KEY"),
        sample_rate=16000
    )
    
    # Initialize LLM service with OpenRouter for Grok-4
    llm = OpenAILLMService(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="x-ai/grok-4",
        base_url="https://openrouter.ai/api/v1",
        default_headers={"HTTP-Referer": "https://yourapp.com"}
    )
    
    # Initialize TTS service
    tts = ElevenLabsTTSService(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        voice_id="nova",
        model="eleven_turbo_v2_5",
        stream=True
    )
    
    # Set up the pipeline
    pipeline = Pipeline([
        transport.input(),
        stt,
        LLMUserResponseAggregator(),
        llm,
        tts,
        transport.output()
    ])
    
    # Create the task
    task = PipelineTask(
        pipeline,
        PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
            enable_usage_metrics=True
        )
    )
    
    # Queue initial system prompt
    initial_messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    await task.queue_frame(LLMMessagesFrame(initial_messages))
    
    # Run the pipeline
    runner = PipelineRunner()
    await runner.run(task)


if __name__ == "__main__":
    asyncio.run(main())