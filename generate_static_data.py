import os
import json
from collections import defaultdict
from datetime import datetime

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(current_dir, "json")
output_folder = os.path.join(current_dir, "json_by_channel_month")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to process and group messages by channel_id and month
def separate_messages_by_channel_and_month():
    # Dictionary to store messages by channel_id and month
    messages_by_channel_month = defaultdict(lambda: defaultdict(list))

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    for item in data:
                        # Extract necessary fields
                        content = item.get('content')
                        timestamp = item.get('timestamp')
                        channel_id = item.get('channel_id')
                        attachments = item.get('attachments', [])

                        # Parse timestamp and determine the month
                        dt = datetime.fromisoformat(timestamp) if timestamp else None
                        month = dt.strftime("%Y-%m") if dt else "unknown"

                        # Handle attachments
                        if attachments:
                            for attachment in attachments:
                                url = attachment.get('url')
                                media_type = get_media_type(url)
                                messages_by_channel_month[channel_id][month].append({
                                    "content": content,
                                    "timestamp": dt.isoformat() if dt else None,
                                    "url": url,
                                    "media_type": media_type
                                })
                        else:
                            messages_by_channel_month[channel_id][month].append({
                                "content": content,
                                "timestamp": dt.isoformat() if dt else None,
                                "url": None,
                                "media_type": "text"
                            })
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {filename}: {e}")

    # Save messages into separate JSON files by channel_id and month
    for channel_id, months in messages_by_channel_month.items():
        for month, messages in months.items():
            output_file = os.path.join(output_folder, f"{channel_id}_{month}.json")
            with open(output_file, 'w', encoding='utf-8') as out_file:
                json.dump(messages, out_file, indent=4)
                print(f"Saved {len(messages)} messages for channel_id {channel_id}, month {month} to {output_file}")

# Determine media type from URL
def get_media_type(url):
    if not url:
        return "text"
    if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return "image"
    if url.endswith(('.mp3', '.m4a')):
        return "audio"
    return "unknown"

# Run the script
if __name__ == "__main__":
    separate_messages_by_channel_and_month()
    print(f"Messages separated by channel_id and month, and saved to {output_folder}")
