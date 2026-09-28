function payWithRazorpay(type) {
  var name = document.getElementById(type === 'customer' ? 'bookName' : 'provName').value;
  var phone = document.getElementById(type === 'customer' ? 'bookPhone' : 'provPhone').value;
  var service = type === 'customer' ? document.getElementById('bookService').value : document.getElementById('provRole').value;
  if(!name || !phone) {
    alert('Please enter your Name and Phone Number first.');
    return;
  }
  var returnUrl = window.location.origin;
  var checkoutUrl = 'https://electra.help/pay.html?amount=200&name=' + encodeURIComponent(name) + '&phone=' + encodeURIComponent(phone) + '&service=' + encodeURIComponent(service) + '&type=' + type + '&redirect=' + encodeURIComponent(returnUrl);
  window.location.href = checkoutUrl;
}
window.addEventListener('DOMContentLoaded', function() {
  var params = new URLSearchParams(window.location.search);
  var paymentId = params.get('payment_id');
  var type = params.get('type') || 'customer';
  if (paymentId) {
    if (type === 'customer') {
      var input = document.getElementById('bookUtr');
      var msg = document.getElementById('bookMsg');
      if (input) input.value = paymentId;
      if (msg) {
        msg.style.color = 'green';
        msg.innerText = 'Payment successful! Reference ID: ' + paymentId;
      }
    } else {
      var input = document.getElementById('provUtr');
      var msg = document.getElementById('provMsg');
      if (input) input.value = paymentId;
      if (msg) {
        msg.style.color: 'green';
        msg.innerText = 'Payment successful! Reference ID: ' + paymentId;
      }
    }
  }
});