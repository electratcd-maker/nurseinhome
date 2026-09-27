export async function onRequestPost(context) {
    try {
        const { username, password } = await context.request.json();
        if (username === "Soniya" && password === "Sumit") {
            return Response.json({ success: true, message: 'Login successful' });
        } else {
            return Response.json({ success: false, message: 'Invalid credentials' }, { status: 401 });
        }
    } catch (err) {
        return Response.json({ success: false, message: err.message }, { status: 500 });
    }
}
