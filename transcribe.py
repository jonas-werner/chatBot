############################################################################
#       _       _   _____     _   _    _                           _ _       
#  ___| |_ ___| |_| __  |___| |_|_|  | |_ ___ ___ ___ ___ ___ ___|_| |_ ___ 
# |  _|   | .'|  _| __ -| . |  _|_   |  _|  _| .'|   |_ -|  _|  _| | . | -_|
# |___|_|_|__,|_| |_____|___|_| |_|  |_| |_| |__,|_|_|___|___|_| |_|___|___|
#                                                                           
############################################################################
# Name: chatBot: Transribe 
# Description: Handles the AWS transcribe portion of the ChatGPT chat bot
# Author: Jonas Werner
# Version: 0.1
############################################################################

import subprocess
import asyncio
import json
import os
import openai
import sounddevice
import requests
import datetime, time
import boto3
import wave

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

AWS_ACCESS_KEY_ID       = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY   = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_DEFAULT_REGION      = os.environ["AWS_DEFAULT_REGION"]


url = "http://localhost:5000/api"
gActive = [0, 1, 1, 1]
message = ""

openai.api_key = os.getenv("OPENAI_API_KEY")

class eventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        global gActive
        global message
        results = transcript_event.transcript.results

        for result in results:
            message = result.alternatives[0].transcript

        if gActive[0] == gActive[1] == gActive[2]:
            if gActive[0] > len(results):

                print("%s" % message)
                #callingOpenAi(message)
                exit(0)

        gActive.insert(0, len(results))

        while(len(gActive) > 5):
            gActive.pop()



async def mic_stream():
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    stream = sounddevice.RawInputStream(
        channels=1,
        callback=callback,
        samplerate=16000,
        blocksize=1024 * 2,
        dtype="int16",
    )

    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe():
    client = TranscribeStreamingClient(region=AWS_DEFAULT_REGION)

    stream = await client.start_stream_transcription(
        #language_code="sv-SE",
        language_code="en-US",
        #language_code="ja-JP",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )

    handler = eventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(stream), handler.handle_events())


loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()


