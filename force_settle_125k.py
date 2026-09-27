import urllib.request
import json
import base64
from datetime import datetime

# Hardcoded Razorpay Credentials[span_2](start_span)[span_2](end_span)
KEY_ID = "rzp_live_SgFENixkcpucYO"
KEY_SECRET = "SSZh3lxXY6YksqE5euEhdMFc"

# Razorpay On-Demand Settlement Endpoint
URL = "https://api.razorpay.com/v1/settlements/ondemand"

# Exactly 125,000 INR converted to paise (125,000 * 100 = 12,500,000)
TARGET_AMOUNT_PAISE = 12500000

payload = {
    "amount": TARGET_AMOUNT_PAISE,
    "settle_full_balance": False,
    "description": "Force settle 125k"
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

print("[*] Dispatching command to Razorpay to settle exactly ₹125,000.00...")

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        
        # Convert values from paise to INR
        req_amt = res_data.get('amount_requested', 0) / 100
        settled_amt = res_data.get('amount_settled', 0) / 100
        pending_amt = res_data.get('amount_pending', 0) / 100
        fees = res_data.get('fees', 0) / 100
        tax = res_data.get('tax', 0) / 100
        
        timestamp = res_data.get('created_at', 0)
        formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        # Comprehensive Financial & Tax Report
        print("\n" + "=" * 58)
        print("         FORCED SETTLEMENT EXECUTION REPORT")
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
        print(" [✓] Settlement request submitted successfully.")

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
    print(" [i] Note: If the error notes insufficient available cleared balance,")
    print("     it means the recent deposits are still clearing through banking rails.")
except Exception as e:
    print(f"\n[-] An unexpected error occurred: {e}")
