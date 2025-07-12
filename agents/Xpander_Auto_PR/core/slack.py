def send_slack_message(text: str):
    from dotenv import load_dotenv
    import os
    import requests
    import json

    load_dotenv()

    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL_ID")

    if not slack_token or not slack_channel:
        print("Slack token or channel missing!")
        return {
            "status": "error",
            "message": "Slack credentials not set in environment variables."
        }

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": slack_channel,
        "text": text,
        "unfurl_links": False
    }

    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            data=json.dumps(payload)
        )
        result = response.json()
        print("Slack API Response:", result)  # DEBUG
        return {"status": "sent" if result.get("ok") else "error", "response": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
