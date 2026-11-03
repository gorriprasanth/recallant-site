// Country-level display preference only; no IP address is read or returned here.
const euro = new Set('AT BE BG HR CY EE FI FR DE GR IE IT LV LT LU MT NL PT SK SI ES AD MC SM VA'.split(' '));
export function currencyResponse(request) {
  if (!['GET', 'HEAD'].includes(request.method)) return new Response(null, {status:405, headers:{Allow:'GET, HEAD','Cache-Control':'private, no-store'}});
  const country = request.cf?.country;
  const currency = country === 'IN' ? 'INR' : country === 'GB' ? 'GBP' : euro.has(country) ? 'EUR' : /^[A-Z]{2}$/.test(country || '') && !['XX','T1'].includes(country) ? 'USD' : 'INR';
  return new Response(request.method === 'HEAD' ? null : JSON.stringify({currency}), {headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff'}});
}
