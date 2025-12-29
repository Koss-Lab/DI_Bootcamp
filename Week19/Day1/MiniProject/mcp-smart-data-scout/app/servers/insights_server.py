# app/servers/insights_server.py

def analyze(text: str) -> dict:
    """
    Simple sentiment analysis tool.
    """
    sentiment = "negative" if "terrible" in text.lower() else "neutral"
    return {
        "sentiment": sentiment,
        "length": len(text),
    }
