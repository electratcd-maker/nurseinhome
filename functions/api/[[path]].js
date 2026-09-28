export async function onRequest(context) {
  const url = new URL(context.request.url);
  const targetUrl = `https://nurseinhome.onrender.com${url.pathname}${url.search}`;
  
  const newHeaders = new Headers(context.request.headers);
  newHeaders.set('Host', 'nurseinhome.onrender.com');

  const proxyRequest = new Request(targetUrl, {
    method: context.request.method,
    headers: newHeaders,
    body: ['GET', 'HEAD'].includes(context.request.method) ? null : context.request.body,
    redirect: 'follow'
  });

  return fetch(proxyRequest);
}
