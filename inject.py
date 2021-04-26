#! /bin/python

import os
import sys
import subprocess
import time
import requests
import asyncio
import websockets
import json

windows = False
port = 9222
if os.name == "nt":
    windows = True

print("launching spotify")
if windows:
    print("windows")
else:
    p = subprocess.Popen(["spotify", f"--remote-debugging-port={port}"])
    time.sleep(5)

with open('style.css', 'r') as file:
    stylesheet = file.read()

while True:
    try:
        data = requests.get(f"http://localhost:{port}/json").json()
        if not data:
            continue
    except:
        continue
    break

ws_uri = data[0]['webSocketDebuggerUrl']

script = f"""
var style  = document.createElement('style');
style.textContent = `
{stylesheet}`;
document.head.append(style);
console.log('css injected!');
"""
print(script, end='')
payload = {
    'id': 69420,
    'method': 'Runtime.evaluate',
    'params': {'expression': script}}

async def inject(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(payload))
        await websocket.recv()

asyncio.get_event_loop().run_until_complete(inject(ws_uri))
