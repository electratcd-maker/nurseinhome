const express = require("express");
const Razorpay = require("razorpay");

const app = express();
app.use(express.json());
app.use(express.static("public"));

const razorpay = new Razorpay({
  key_id: process.env.RAZORPAY_KEY_ID || "rzp_live_dummy",
  key_secret: process.env.RAZORPAY_KEY_SECRET || "dummy_secret"
});

let bookings = [];
let providers = [];

// 1. Founder endpoint
app.get("/api/founder", (req, res) => {
  res.json({
    success: true,
    founder: { name: "Soniya Pal", qualification: "MSc Nursing", role: "Founder & Chief Nursing Officer" }
  });
});

// 2. Order creation endpoint
app.post("/api/create-order", async (req, res) => {
  try {
    const { amount } = req.body;
    const order = await razorpay.orders.create({
      amount: (amount || 200) * 100,
      currency: "INR",
      receipt: "rcpt_" + Date.now()
    });
    res.json({ success: true, order, key_id: razorpay.key_id });
  } catch (err) {
    console.error("Order error:", err);
    res.status(500).json({ success: false, message: err.message });
  }
});

// 3. Customer Booking submission
app.post("/api/book", (req, res) => {
  const { name, phone, service, address, utr } = req.body;
  if (!name || !phone || !utr) {
    return res.status(400).json({ success: false, message: "Missing required fields" });
  }
  const booking = { id: Date.now(), name, phone, service, address, utr, date: new Date().toISOString() };
  bookings.push(booking);
  console.log("New Booking Saved:", booking);
  res.json({ success: true, message: "Booking registered successfully!", booking });
});

// 4. Provider Registration submission
app.post("/api/register", (req, res) => {
  const { name, phone, role, exp, address, utr } = req.body;
  if (!name || !phone || !utr) {
    return res.status(400).json({ success: false, message: "Missing required fields" });
  }
  const provider = { id: Date.now(), name, phone, role, exp, address, utr, date: new Date().toISOString() };
  providers.push(provider);
  console.log("New Provider Saved:", provider);
  res.json({ success: true, message: "Provider registered successfully!", provider });
});

// 5. Admin Endpoints
app.get("/api/admin/bookings", (req, res) => res.json({ success: true, bookings }));
app.get("/api/admin/providers", (req, res) => res.json({ success: true, providers }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Server running on port " + PORT));
