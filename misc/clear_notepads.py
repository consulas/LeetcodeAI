from prompts import *
from util import *
from notepad import *
import os
import requests
settings = {'maxtokens': 2048, 'chunktokens': 64, 'temperature': 1, 'top_k': 0, 'top_p': 0, 'min_p': 0.05, 'tfs': 0.0, 'mirostat': False, 'mirostat_tau': 1.25, 'mirostat_eta': 0.1, 'typical': 0.0, 'repp': 1.01, 'repr': 1024, 'repd': 512, 'quad_sampling': 0.0, 'temperature_last': False, 'skew': 0.0, 'stop_conditions': [{'text': '</s>', 'inclusive': False}, {'text': '<|eot_id|>', 'inclusive': True}], 'dry_base': 1.75, 'dry_multiplier': 0.0, 'dry_range': 1024}
headers = {'Content-Type': 'application/json'}
test_notepad = Notepad("http://localhost:5000", settings=settings)
notepads = test_notepad.list_notepads()

# Clear all notepads with delete value
for key, value in notepads.items():
    if value == 'Delete':
        data = {'notepad_uuid': key}
        response = requests.post(f"http://localhost:5000/api/delete_notepad", headers=headers, json=data)
