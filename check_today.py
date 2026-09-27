import urllib.request
import json
import base64
from datetime import datetime, time

# Hardcoded Razorpay Credentials[span_1](start_span)[span_1](end_span)
KEY_ID = "rzp_live_SgFENixkcpucYO"
KEY_SECRET = "SSZh3lxXY6YksqE5euEhdMFc"

# Razorpay On-Demand Settlements Endpoint
URL = "https://api.razorpay.com/v1/settlements/ondemand"

credentials = f"{KEY_ID}:{KEY_SECRET}"
encoded_auth = base64.b64encode(credentials.encode('ascii')).decode('ascii')

req = urllib.request.Request(
    URL,
    headers={
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    },
    method="GET"
)

print("[*] Fetching settlement history from Razorpay...")

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        items = res_data.get('items', [])
        
        # Get start of today (midnight 00:00:00) timestamp
        now = datetime.now()
        start_of_today = datetime.combine(now.date(), time.min).timestamp()
        
        total_today = 0
        count_today = 0
        
        print("\n" + "=" * 54)
        print("        SETTLEMENTS PROCESSED / CREATED TODAY")
        print("=" * 54)
        
        for item in items:
            created_at = item.get('created_at', 0)
            if created_at >= start_of_today:
                # Use amount_requested or amount_settled
                amt = (item.get('amount_requested', 0)) / 100
                status = item.get('status', '').upper()
                time_str = datetime.fromtimestamp(created_at).strftime('%H:%M:%S')
                
                print(f" • ID: {item.get('id')}")
                print(f"   Time: {time_str} | Status: {status} | Amount: ₹{amt:,.2f}")
                print("-" * 54)
                
                total_today += amt
                count_today += 1
                
        print(f" [i] Total Requests Today : {count_today}")
        print(f" [✓] Total Amount Today   : ₹{total_today:,.2f}")
        print("=" * 54)

except urllib.error.HTTPError as e:
    print(f"\n[-] HTTP Error: {e.code} - {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"\n[-] An unexpected error occurred: {e}")
