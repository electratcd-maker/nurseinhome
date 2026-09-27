import urllib.request
import json
import base64
from datetime import datetime, time, timedelta

# Hardcoded Razorpay Credentials[span_1](start_span)[span_1](end_span)
KEY_ID = "rzp_live_SgFENixkcpucYO"
KEY_SECRET = "SSZh3lxXY6YksqE5euEhdMFc"

credentials = f"{KEY_ID}:{KEY_SECRET}"
encoded_auth = base64.b64encode(credentials.encode('ascii')).decode('ascii')
headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/json"
}

# 1. Calculate timestamp for 4 months ago (approx 120 days)
now = datetime.now()
four_months_ago = now - timedelta(days=120)
start_timestamp = int(four_months_ago.timestamp())

print("[*] Querying Razorpay for past 4 months received payments...")
payments_url = f"https://api.razorpay.com/v1/payments?from={start_timestamp}&count=100"
req_payments = urllib.request.Request(payments_url, headers=headers, method="GET")

total_received_4m = 0
payment_count = 0

try:
    with urllib.request.urlopen(req_payments) as response:
        data = json.loads(response.read().decode('utf-8'))
        items = data.get('items', [])
        for p in items:
            # Sum up successfully captured payments
            if p.get('status') == 'captured':
                total_received_4m += p.get('amount', 0) / 100
                payment_count += 1
except urllib.error.HTTPError as e:
    print(f"[-] Payments API Error: {e.code} - {e.reason}")
except Exception as e:
    print(f"[-] Error fetching payments: {e}")

print("[*] Querying Razorpay for today's settlements...")
settlements_url = "https://api.razorpay.com/v1/settlements/ondemand"
req_settlements = urllib.request.Request(settlements_url, headers=headers, method="GET")

total_settled_today = 0
settlement_count_today = 0
start_of_today = datetime.combine(now.date(), time.min).timestamp()

try:
    with urllib.request.urlopen(req_settlements) as response:
        data = json.loads(response.read().decode('utf-8'))
        items = data.get('items', [])
        for s in items:
            created_at = s.get('created_at', 0)
            if created_at >= start_of_today:
                total_settled_today += s.get('amount_requested', 0) / 100
                settlement_count_today += 1
except urllib.error.HTTPError as e:
    print(f"[-] Settlements API Error: {e.code} - {e.reason}")
except Exception as e:
    print(f"[-] Error fetching settlements: {e}")

# Comprehensive Clean Report
print("\n" + "=" * 54)
print("             COMPREHENSIVE FINANCIAL REPORT")
print("=" * 54)
print(f" [i] Report Generated : {now.strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 54)
print(f" • Total Received (Past 4 Months) : ₹{total_received_4m:,.2f}")
print(f"   (Successful Payments Count   : {payment_count})")
print("-" * 54)
print(f" • Total Settled/Queued Today     : ₹{total_settled_today:,.2f}")
print(f"   (Settlement Requests Today   : {settlement_count_today})")
print("=" * 54)
print(" [✓] Summary generated successfully.")
