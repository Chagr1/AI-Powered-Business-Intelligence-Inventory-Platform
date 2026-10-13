
import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY could not be loaded from the .env file!")
else:
    print(f"API Key Prefix: {api_key[:8]}...")

    client = Groq(api_key=api_key)

    try:
        print("\n--- MODELS CURRENTLY AVAILABLE AND AUTHORIZED FOR YOUR ACCOUNT ---")

        models = client.models.list()

        for model in models.data:
            print(model.id)

    except Exception as e:
        print("An error occurred while connecting to the API:", e)
