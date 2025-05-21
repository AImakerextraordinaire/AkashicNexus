#Bridge for integration into KoboldCpp
import requests

KOBOLD_ENDPOINT = "http://localhost:5001/api/v1/generate"

def local_generate(prompt, max_tokens=300, temperature=0.8, top_p=0.95, stop_sequences=None):
    """
    Sends a prompt to a running KoboldCPP instance and returns the generated response.
    """
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "stop_sequence": stop_sequences or []
    }

    try:
        response = requests.post(KOBOLD_ENDPOINT, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["results"][0]["text"].strip()

    except requests.RequestException as e:
        print(f"[kobold_bridge] ?? Error communicating with KoboldCPP: {e}")
        return "[Error: KoboldCPP unavailable]"

    except (KeyError, IndexError):
        return "[Error: Malformed response from KoboldCPP]"

