import urllib.request
import json
import base64

# Hardcoded Razorpay Credentials[span_0](start_span)[span_0](end_span)
KEY_ID = "rzp_live_SgFENixkcpucYO"
KEY_SECRET = "SSZh3lxXY6YksqE5euEhdMFc"

# Razorpay On-Demand Settlement Endpoint
URL = "https://api.razorpay.com/v1/settlements/ondemand"

# Payload with description shortened to fit the <= 30 character limit
payload = {
    "settle_full_balance": True,
    "description": "Termux settlement"
}

# Encode credentials for HTTP Basic Authentication
credentials = f"{KEY_ID}:{KEY_SECRET}"
encoded_auth = base64.b64encode(credentials.encode('ascii')).decode('ascii')

req = urllib.request.Request(
    URL,
    data=json.dumps(payload).encode('utf-8'),
    headers={
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    },
    method="POST"
)

print("[*] Initiating request to settle full waiting balance...")

try:
    with urllib.request.urlopen(req) as response:
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)
        print("\n[+] Settlement Successfully Triggered!")
        print(json.dumps(result, indent=4))
except urllib.error.HTTPError as e:
    print(f"\n[-] HTTP Error: {e.code} - {e.reason}")
    error_body = e.read().decode('utf-8')
    print(error_body)
except Exception as e:
    print(f"\n[-] An unexpected error occurred: {e}")
