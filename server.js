const express = require('express');
const path = require('path');
const Razorpay = require('razorpay');
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Corrected lowercase Razorpay Live Credentials
const razorpay = new Razorpay({
    key_id: 'rzp_live_SgFENixkcpucYO',
    key_secret: 'SSZh3lxXY6YksqE5euEhdMFc'
});

let bookings = [];
let providers = [];

const ADMIN_USER = "Soniya";
const ADMIN_PASS = "Sumit";

// Founder Profile Information
const FOUNDER = {
    name: "Soniya Pal",
    qualification: "MSc Nursing",
    role: "Founder & Chief Nursing Officer"
};

// API to get Founder details
app.get('/api/founder', (req, res) => {
    res.json({ success: true, founder: FOUNDER });
});

// Create Razorpay Order for ₹200 Fee with detailed error logging
app.post('/api/create-order', async (req, res) => {
    try {
        const options = {
            amount: 200 * 100, // ₹200 in paise
            currency: "INR",
            receipt: "rcpt_" + Date.now()
        };
        const order = await razorpay.orders.create(options);
        res.json({ success: true, order, key_id: 'rzp_live_SgFENixkcpucYO' });
    } catch (err) {
        console.error("Razorpay Order Creation Error:", err);
        res.status(500).json({ success: false, message: err.error ? err.error.description : err.message });
    }
});

// Customer Booking API
app.post('/api/book', (req, res) => {
    const { name, phone, serviceType, address, razorpay_payment_id } = req.body;
    if (!name || !phone || !serviceType || !address) {
        return res.status(400).json({ success: false, message: 'All booking fields are required.' });
    }
    const booking = { 
        id: 'BK-' + Date.now().toString().slice(-5), 
        name, 
        phone, 
        serviceType, 
        address, 
        paymentId: razorpay_payment_id || 'Paid via Razorpay',
        fee: '₹200',
        date: new Date().toISOString() 
    };
    bookings.push(booking);
    res.json({ success: true, message: 'Booking & ₹200 payment collected successfully!', booking });
});

app.get('/api/admin/bookings', (req, res) => {
    res.json({ success: true, bookings });
});

// Professional Provider Registration API
app.post('/api/provider/register', (req, res) => {
    const { name, phone, role, experience, address, razorpay_payment_id } = req.body;
    if (!name || !phone || !role || !experience || !address) {
        return res.status(400).json({ success: false, message: 'All registration fields are required.' });
    }
    const provider = { 
        id: 'PRV-' + Date.now().toString().slice(-5), 
        name, 
        phone, 
        role, 
        experience, 
        address, 
        paymentId: razorpay_payment_id || 'Paid via Razorpay', 
        fee: '₹200',
        date: new Date().toISOString() 
    };
    providers.push(provider);
    res.json({ success: true, message: 'Professional registration & ₹200 fee collected successfully!', provider });
});

app.get('/api/admin/providers', (req, res) => {
    res.json({ success: true, providers });
});

// Admin Login API
app.post('/api/admin/login', (req, res) => {
    const { username, password } = req.body;
    if (username === ADMIN_USER && password === ADMIN_PASS) {
        res.json({ success: true, message: 'Login successful' });
    } else {
        res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
});

app.listen(3000, () => {
    console.log('NurseInHome server running at http://localhost:3000');
});
