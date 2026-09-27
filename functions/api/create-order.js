export async function onRequestPost(context) {
    try {
        const key_id = 'rzp_live_SgFENixkcpucYO';
        const key_secret = 'SSZh3lxXY6YksqE5euEhdMFc';
        
        const auth = btoa(`${key_id}:${key_secret}`);
        const response = await fetch('https://api.razorpay.com/v1/orders', {
            method: 'POST',
            headers: {
                'Authorization': `Basic ${auth}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amount: 200 * 100, // ₹200 in paise
                currency: "INR",
                receipt: "rcpt_" + Date.now()
            })
        });

        const order = await response.json();
        if (!response.ok) throw new Error(order.error?.description || 'Razorpay order failed');

        return Response.json({ success: true, order, key_id });
    } catch (err) {
        return Response.json({ success: false, message: err.message }, { status: 500 });
    }
}
