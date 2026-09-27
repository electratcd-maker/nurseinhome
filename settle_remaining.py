import urllib.request
import json
import base64
from datetime import datetime

# Hardcoded Razorpay Credentials[span_1](start_span)[span_1](end_span)
KEY_ID = "rzp_live_SgFENixkcpucYO"
KEY_SECRET = "SSZh3lxXY6YksqE5euEhdMFc"

# Razorpay On-Demand Settlement Endpoint
URL = "https://api.razorpay.com/v1/settlements/ondemand"

payload = {
    "settle_full_balance": True,
    "description": "Final balance sweep"
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

print("[*] Initiating final sweep for remaining unsettled balance...")

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        
        # Convert values from paise to INR
        req_amt = res_data.get('amount_requested', 0) / 100
        settled_amt = res_data.get('amount_settled', 0) / 100
        pending_amt = res_data.get('amount_pending', 0) / 100
        fees = res_data.get('fees', 0) / 100
        tax = res_data.get('tax', 0) / 100
        
        # Format Timestamp
        timestamp = res_data.get('created_at', 0)
        formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        # Comprehensive Financial Report
        print("\n" + "=" * 54)
        print("        FINAL SETTLEMENT & BALANCE REPORT")
        print("=" * 54)
        print(f" [i] Settlement ID    : {res_data.get('id')}")
        print(f" [i] Current Status   : {res_data.get('status').upper()}")
        print(f" [i] Timestamp        : {formatted_date}")
        print("-" * 54)
        print(f" • Total Requested    : ₹{req_amt:,.2f}")
        print(f" • Processing Fees    : ₹{fees:,.2f}")
        print(f" • Tax (GST)          : ₹{tax:,.2f}")
        print(f" • Amount Received    : ₹{settled_amt:,.2f}")
        print(f" • Still Pending      : ₹{pending_amt:,.2f}")
        print("=" * 54)
        print(" [✓] Sweep request processed successfully.")

except urllib.error.HTTPError as e:
    print(f"\n[-] HTTP Error: {e.code} - {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"\n[-] An unexpected error occurred: {e}")
