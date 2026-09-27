import http.server
import socketserver
import json
import urllib.request
import base64

PORT = 3001
KEY_ID = "rzp_live_SgFENixkcpucYO"
KEY_SECRET = "SSZh3lxXY6YksqE5euEhdMFc"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Razorpay Custom Payment UI</title>
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; width: 330px; }
        h2 { margin-bottom: 10px; color: #333; }
        p { color: #666; font-size: 14px; margin-bottom: 20px; }
        input { width: 90%; padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 20px; text-align: center; }
        button { background-color: #3399cc; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { background-color: #287b33; }
        #status { margin-top: 15px; font-size: 14px; color: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Razorpay Portal</h2>
        <p>Enter custom amount to pay</p>
        <input type="number" id="amount" placeholder="Amount in INR (e.g. 500)" step="1" min="1">
        <br>
        <button id="pay-btn">Pay Now</button>
        <div id="status"></div>
    </div>

    <script>
        document.getElementById('pay-btn').onclick = async function (e) {
            const amount = document.getElementById('amount').value;
            const statusDiv = document.getElementById('status');

            if (!amount || amount <= 0) {
                alert('Please enter a valid amount.');
                return;
            }

            statusDiv.innerText = "Creating order...";

            try {
                const response = await fetch('/create-order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ amount: amount })
                });

                const order = await response.json();
                if (order.error) {
                    statusDiv.innerText = "Error: " + order.error;
                    return;
                }

                statusDiv.innerText = "";

                const options = {
                    "key": "${KEY_ID}",
                    "amount": order.amount,
                    "currency": "INR",
                    "name": "Custom Merchant Payment",
                    "description": "Test Transaction",
                    "order_id": order.id,
                    "handler": function (response){
                        alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                        statusDiv.innerText = "Success! ID: " + response.razorpay_payment_id;
                    },
                    "theme": { "color": "#3399cc" }
                };

                const rzp = new Razorpay(options);
                rzp.open();
            } catch (err) {
                statusDiv.innerText = "Transaction failed to initialize.";
                console.error(err);
            }
        }
    </script>
</body>
</html>
"""

class PaymentHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/create-order':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            amount_in_inr = float(data.get('amount', 100))
            amount_in_paise = int(amount_in_inr * 100)

            order_data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1
            }
            
            req_url = "https://api.razorpay.com/v1/orders"
            credentials = f"{KEY_ID}:{KEY_SECRET}"
            encoded_auth = base64.b64encode(credentials.encode('ascii')).decode('ascii')
            
            req = urllib.request.Request(req_url, data=json.dumps(order_data).encode('utf-8'), headers={
                "Authorization": f"Basic {encoded_auth}",
                "Content-Type": "application/json"
            })
            
            try:
                with urllib.request.urlopen(req) as response:
                    response_data = response.read().decode('utf-8')
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(response_data.encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

print(f"[*] Starting local Python server on http://localhost:{PORT}")
with ReusableTCPServer(("", PORT), PaymentHandler) as httpd:
    httpd.serve_forever()
