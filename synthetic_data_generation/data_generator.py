import json
import logging
from typing import List, Dict
from llm_handler import LLMHandler

logging.basicConfig(level=logging.INFO)


class DataGenerator:
    def __init__(self, schema: Dict, llm_handler: LLMHandler):
        self.schema = schema
        self.llm_handler = llm_handler

    def generate(self, seed_data: List[Dict], num_samples: int) -> List[Dict]:
        synthetic_data = []
        for _ in range(num_samples):
            for example in seed_data:
                prompt = (
                    f"Generate a similar data entry based on this example:\n{example}\n"
                    f"Output the result as a JSON object with the following keys: {list(self.schema.keys())}."
                )
                generated_text = self.llm_handler.query(prompt, {"max_tokens": 500})
                logging.info(f"Generated text: {generated_text}")

                try:
                    synthetic_entry = self._parse_generated_data(generated_text)
                    synthetic_data.append(synthetic_entry)
                except ValueError as e:
                    logging.error(f"Failed to parse generated data: {e}")
        return synthetic_data

    def _parse_generated_data(self, generated_text: str) -> Dict:
        try:
            # Remove Markdown code block delimiters if present
            if generated_text.startswith("```") and "```" in generated_text[3:]:
                generated_text = generated_text.strip("```json").strip("```")

            # Parse the cleaned text as JSON
            return json.loads(generated_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing generated data as JSON: {e}\nGenerated text: {generated_text}")
