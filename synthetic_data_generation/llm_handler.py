from typing import Dict, Any


class LLMHandler:
    def __init__(self, model: str, api_key: str = None):
        self.model = model
        self.api_key = api_key

    def query(self, prompt: str, parameters: Dict[str, Any]) -> str:
        if self.model.startswith("openai"):
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = [
                {"role": "developer", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]

            # Call the OpenAI chat completions endpoint
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                **parameters
            )

            # Return the first response message
            return response.choices[0].message.content.strip()
        elif self.model == "huggingface":
            from transformers import pipeline
            generator = pipeline("text-generation", model=self.api_key)
            response = generator(prompt, **parameters)
            return response[0]["generated_text"]
        elif self.model == "local":
            # Add support for a local model
            raise NotImplementedError("Local model support is not implemented yet.")
        else:
            raise ValueError("Unsupported model specified.")
