import os
from pathlib import Path
from dotenv import load_dotenv
from runwayml import RunwayML

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = RunwayML(
    api_key=os.getenv("RUNWAY_API_KEY")
)

print("✅ Connected to Runway SDK")