from google.generativeai import generative_models
from google.generativeai import types
import google.generativeai as genai
import json
import base64
import pathlib
import pprint
import requests
import mimetypes


#Апи ключ
API_KEY=userdata.get('API_KEY')

genai.configure(api_key=API_KEY)

#Название языковой модели и конфигурации
model = 'gemini-1.0-pro' # @param {isTemplate: true}
contents_b64 = 'W10=' # @param {isTemplate: true}
generation_config_b64 = 'eyJ0ZW1wZXJhdHVyZSI6MC45LCJ0b3BfcCI6MSwidG9wX2siOjEsIm1heF9vdXRwdXRfdG9rZW5zIjoyMDQ4LCJzdG9wX3NlcXVlbmNlcyI6W119' # @param {isTemplate: true}
safety_settings_b64 = 'W3siY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX0hBUkFTU01FTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfSEFURV9TUEVFQ0giLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfU0VYVUFMTFlfRVhQTElDSVQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfREFOR0VST1VTX0NPTlRFTlQiLCJ0aHJlc2hvbGQiOiJCTE9DS19NRURJVU1fQU5EX0FCT1ZFIn1d' # @param {isTemplate: true}
user_input_b64 = '' # @param {isTemplate: true}

contents = json.loads(base64.b64decode(contents_b64))
generation_config = json.loads(base64.b64decode(generation_config_b64))
safety_settings = json.loads(base64.b64decode(safety_settings_b64))
user_input = base64.b64decode(user_input_b64).decode()
stream = False

contents = []

generation_config = {'temperature': 0.9,
 'top_p': 1,
 'top_k': 1,
 'max_output_tokens': 4096,
 'stop_sequences': []}

safety_settings = [{'category': 'HARM_CATEGORY_HARASSMENT',
  'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
 {'category': 'HARM_CATEGORY_HATE_SPEECH',
  'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
 {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
  'threshold': 'BLOCK_MEDIUM_AND_ABOVE'},
 {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
  'threshold': 'BLOCK_MEDIUM_AND_ABOVE'}]

#Ввод текста пользователем
user_input = ''

# Вызов апи и ответ модели
gemini = genai.GenerativeModel(model_name=model)

chat = gemini.start_chat(history=contents)

response = chat.send_message(
    user_input,
    stream=stream)

print(response.text)

response.prompt_feedback
response.candidates
