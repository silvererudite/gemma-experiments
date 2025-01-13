# orchestrator.py
from schema import Schema
from llm_handler import LLMHandler
from data_generator import DataGenerator
import json


def main():
    # Load example dataset
    with open("seed_data.json", "r") as f:
        seed_data = json.load(f)

    # Define schema
    schema = {
        "query": str,
        "expected_answer": str,
        "type": str,
        "region": str,
        "intent": str,
    }
    schema_validator = Schema(schema)
    schema_validator.validate(seed_data)

    # Initialize LLM Handler
    llm_handler = LLMHandler(model="openai", api_key="...")

    # Generate synthetic data
    generator = DataGenerator(schema=schema, llm_handler=llm_handler)
    synthetic_data = generator.generate(seed_data, num_samples=20)

    # Save synthetic data
    with open("synthetic_data.json", "w") as f:
        json.dump(synthetic_data, f, indent=4)
    print("Synthetic data saved to synthetic_data.json.")


if __name__ == "__main__":
    main()
