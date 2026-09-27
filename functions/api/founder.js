export async function onRequestGet(context) {
    const FOUNDER = {
        name: "Soniya Pal",
        qualification: "MSc Nursing",
        role: "Founder & Chief Nursing Officer"
    };
    return Response.json({ success: true, founder: FOUNDER });
}
