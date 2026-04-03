import os
import google.generativeai as genai
from config import settings

genai.configure(api_key="AIzaSyCLq69guhG_42GhO-S2FM8MMtN5qhtdsGg")

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
