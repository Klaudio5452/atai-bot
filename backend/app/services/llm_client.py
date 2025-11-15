# app/services/llm_client.py
import os

class LLMClient:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
        if not self.mock_mode:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None

    def complete(self, prompt: str, temperature: float = 0.7) -> str:
        # If mock mode is enabled, return a simulated AI response
        if self.mock_mode:
            print("[MOCK MODE] Returning fake AI response.")
            return f"[Mock AI] You asked: '{prompt}'. This is a simulated response."

        # Otherwise, call the real OpenAI API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI travel assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("[LLMClient ERROR]", str(e))
            return f"[Error contacting AI]: {str(e)}"
