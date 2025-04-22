import os
import requests

def verify(token: str, remote_ip: str | None = None) -> bool:
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': os.getenv("CAPTCHA_SITE_SECRET"),
        'response': token,
    }

    if remote_ip is not None:
        payload['remoteip'] = remote_ip

    try:
        response = requests.post(url, data=payload)
        result = response.json()
        return result.get("success")    

    except requests.RequestException as e:
        print(f"reCAPTCHA verification failed: {e}")
        return False
