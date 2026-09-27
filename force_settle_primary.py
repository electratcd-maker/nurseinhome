import urllib.request
import json
import base64
from datetime import datetime

# Primary Razorpay Credentials from Source Document[span_1](start_span)[span_1](end_span)
KEY_ID = "Rzp_live_RqeccVf9XQVWCS"
KEY_SECRET = "R3Ro90Y03rJInfvmUrHTytKI"

# Razorpay On-Demand Settlement Endpoint
URL = "https://api.razorpay.com/v1/settlements/ondemand"

# Exactly 125,000 INR converted to paise (125,000 * 100 = 12,500,000)
TARGET_AMOUNT_PAISE = 12500000

payload = {
    "amount": TARGET_AMOUNT_PAISE,
    "settle_full_balance": False,
    "description": "Primary force settle 125k"
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

print("[*] Dispatching command via PRIMARY account credentials to settle ₹125,000.00...")

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        
        req_amt = res_data.get('amount_requested', 0) / 100
        settled_amt = res_data.get('amount_settled', 0) / 100
        pending_amt = res_data.get('amount_pending', 0) / 100
        fees = res_data.get('fees', 0) / 100
        tax = res_data.get('tax', 0) / 100
        
        timestamp = res_data.get('created_at', 0)
        formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        print("\n" + "=" * 58)
        print("     PRIMARY ACCOUNT FORCED SETTLEMENT REPORT")
        print("=" * 58)
        print(f" [i] Settlement ID    : {res_data.get('id')}")
        print(f" [i] Current Status   : {res_data.get('status').upper()}")
        print(f" [i] Timestamp        : {formatted_date}")
        print("-" * 58)
        print(f" • Target Requested   : ₹{req_amt:,.2f}")
        print(f" • Processing Fees    : ₹{fees:,.2f}")
        print(f" • Legal Tax (GST)    : ₹{tax:,.2f}")
        print(f" • Net Settled Amount : ₹{settled_amt:,.2f}")
        print(f" • Remaining Available: ₹{pending_amt:,.2f}")
        print("=" * 58)
        print(" [✓] Settlement request submitted successfully via primary account.")

except urllib.error.HTTPError as e:
    print("\n" + "=" * 58)
    print("      [!] ERROR ENCOUNTERED - RAW JSON RESPONSE")
    print("=" * 58)
    print(f" HTTP Status Code: {e.code} ({e.reason})")
    try:
        error_body = e.read().decode('utf-8')
        parsed_json = json.loads(error_body)
        print(json.dumps(parsed_json, indent=4))
    except Exception:
        print(e.read().decode('utf-8'))
    print("=" * 58)
except Exception as e:
    print(f"\n[-] An unexpected error occurred: {e}")
