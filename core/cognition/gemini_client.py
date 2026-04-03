import os
import google.generativeai as genai
from django.conf import settings

class GeminiClient:
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in settings")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    def generate_response(self, prompt, system_instruction=None):
        """
        Generates a response from Gemini given a prompt and optional system instruction.
        """
        try:
            if system_instruction:
                # Re-initialize with system instruction if provided
                model = genai.GenerativeModel(
                    'gemini-1.5-flash-latest',
                    system_instruction=system_instruction
                )
            else:
                model = self.model

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None
