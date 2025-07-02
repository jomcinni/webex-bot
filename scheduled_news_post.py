def summarize_article(article_text):
    import requests
    import json
    import os

    API_URL = "https://chat-ai.cisco.com/openai/deployments/gpt-4o-mini/chat/completions"
    API_KEY = os.environ["CIRCUIT_API_KEY"]  # Set this as a GitHub secret
    APP_KEY = os.environ["CIRCUIT_APP_KEY"]  # Set this as a GitHub secret

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api-key": API_KEY
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": f"Summarize this article: {article_text}"}
        ],
        "user": json.dumps({"appkey": APP_KEY}),
        "stop": ["<|im_end|>"]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Summarization API error: {response.status_code} {response.text}")
            return "Summary unavailable."
    except Exception as e:
        print(f"Summarization API exception: {e}")
        return "Summary unavailable."
