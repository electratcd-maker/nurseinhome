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

app.get("/api/founder", (req, res) => {
  res.json({
    success: true,
    founder: { name: "Soniya Pal", qualification: "MSc Nursing", role: "Founder & Chief Nursing Officer" }
  });
});

app.post("/api/create-payment-link", async (req, res) => {
  try {
    const { name, phone, type, service } = req.body;

    const paymentLink = await razorpay.paymentLink.create({
      amount: 20000,
      currency: "INR",
      accept_partial: false,
      description: `NurseInHome ${type === "customer" ? "Booking" : "Registration"} - ${service || "Care Service"}`,
      customer: { name: name || "Customer", contact: phone || "" },
      notify: { sms: true, email: false },
      callback_url: "https://nurseinhome.in/",
      callback_method: "get"
    });

    res.json({ success: true, payment_url: paymentLink.short_url });
  } catch (error) {
    console.error("Error creating payment link:", error);
    res.status(500).json({ success: false, message: error.message });
  }
});

app.get("/api/admin/bookings", (req, res) => res.json({ success: true, bookings }));
app.get("/api/admin/providers", (req, res) => res.json({ success: true, providers }));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
