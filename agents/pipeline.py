import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scene_generator import generate_scenes
from character_extractor import extract_characters

print("=" * 60)
print("🚀 DOCUMENTARY AI PIPELINE")
print("=" * 60)

print("\nSTEP 1 : Scene Generator")
generate_scenes()

print("\nSTEP 2 : Character Extractor")
extract_characters()

print("\n✅ Pipeline completed successfully!")