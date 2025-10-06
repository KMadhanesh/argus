# argus/orpheus/services/gemini_client.py

import requests
import time
from .. import config

def query(prompt: str) -> tuple[str | None, str | None]:
    """
    Centralized function to send a prompt to the Gemini API.

    This service encapsulates all the logic for making the API call,
    including API key management, request formatting, and a resilient
    "exponential backoff" retry strategy. This prevents code duplication
    across different handlers.

    Args:
        prompt (str): The fully constructed prompt to be sent to the AI.

    Returns:
        tuple[str | None, str | None]: A tuple containing the AI's response text
                                       on success (and None for the error), or
                                       None for the response and an error message
                                       on failure.
    """
    api_key = config.GEMINI_API_KEY
    if not api_key:
        return None, "GEMINI_API_KEY not found in configuration."

    # aponta para o gemini-1.5-flash-latest
    # api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # aponta para o gemini-2.5-pro
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    max_retries = 3
    base_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            
            json_response = response.json()
            answer = json_response['candidates'][0]['content']['parts'][0]['text']
            return answer.strip(), None

        except requests.exceptions.RequestException as e:
            # Using hasattr to safely check for response before accessing it.
            if hasattr(e, 'response') and e.response is not None and 500 <= e.response.status_code < 600:
                print(f"⚠️ Server error ({e.response.status_code}). Attempt {attempt + 1} of {max_retries}...")
                time.sleep(base_delay * (2 ** attempt))
                continue
            else:
                return None, f"Error communicating with the Gemini API: {e}"
        except (KeyError, IndexError):
             return None, "Unexpected response format from the Gemini API."

    return None, "The Gemini server remains unavailable after several attempts."