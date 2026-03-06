import json
import sys

def validate_workout_file(filepath):
    print(f"--- Checking: {filepath} ---")
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("❌ ERROR: Top level of JSON must be a LIST [].")
            return

        for index, item in enumerate(data):
            # Check for required keys
            if "title" not in item or "url" not in item:
                print(f"❌ ERROR at index {index}: Missing 'title' or 'url'.")
                continue
            
            # Check if URL is a valid YouTube link
            url = item["url"]
            if "youtube.com" not in url and "youtu.be" not in url:
                print(f"⚠️ WARNING at index {index}: '{url}' is not a standard YouTube URL.")
            
            print(f"✅ OK: {item['title']}")

        print(f"\nSummary: {len(data)} workouts validated successfully.")

    except json.JSONDecodeError as e:
        print(f"❌ CRITICAL: Invalid JSON syntax! \nError: {e}")
    except FileNotFoundError:
        print("❌ ERROR: File not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_workouts.py your_file.json")
    else:
        validate_workout_file(sys.argv[1])