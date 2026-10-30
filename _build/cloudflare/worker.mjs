import publicFiles from './public-files.json' with {type:'json'};

const allowed=new Set(publicFiles.map(name=>'/'+name));
const canonical='https://recallant.com';
const security={
 'X-Content-Type-Options':'nosniff',
 'Referrer-Policy':'strict-origin-when-cross-origin',
 'X-Frame-Options':'DENY',
 'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'none'",
 'Permissions-Policy':'camera=(), microphone=(), geolocation=()'
};
function protect(response,{head=false,preview=false,path='',status=response.status}={}){
 const headers=new Headers(response.headers);
 for(const [key,value]of Object.entries(security))headers.set(key,value);
 const html=(headers.get('Content-Type')||'').toLowerCase().startsWith('text/html');
 const cache=preview||status>=300?'no-store':html?'public, max-age=0, must-revalidate':/\.(?:png|jpg|ico|svg|woff2)$/.test(path)?'public, max-age=86400':'public, max-age=300';
 headers.set('Cache-Control',cache+', no-transform');
 if(preview)headers.set('X-Robots-Tag','noindex, nofollow');
 else headers.set('Strict-Transport-Security','max-age=31536000');
 return new Response(head?null:response.body,{status,statusText:status===response.status?response.statusText:'',headers});
}
function text(status,message,headers={}){return new Response(message,{status,headers:{'Content-Type':'text/plain; charset=utf-8',...headers}});}
export default {
 async fetch(request,env){
  const url=new URL(request.url);const head=request.method==='HEAD';const preview=env.DEPLOYMENT_ENV==='preview';const options={head,preview,path:url.pathname};
  if(!['production','preview'].includes(env.DEPLOYMENT_ENV))return protect(text(503,'This site is temporarily unavailable.'),options);
  if(!['GET','HEAD'].includes(request.method))return protect(text(405,'Method not allowed.',{Allow:'GET, HEAD'}),options);
  const assetPath=url.pathname==='/'?'/index.html':url.pathname;
  if(!allowed.has(assetPath)){
   const missing=await env.ASSETS.fetch(new Request(new URL('/404.html',url),{method:'GET'}));
   return protect(missing,{...options,status:404});
  }
  if(!preview){
   if(!['recallant.com','www.recallant.com'].includes(url.hostname))return protect(text(421,'Use recallant.com.'),options);
   if(url.origin!==canonical)return protect(new Response(null,{status:308,headers:{Location:canonical+url.pathname+url.search}}),options);
  }
  if(preview&&url.pathname==='/robots.txt')return protect(text(200,'User-agent: *\nDisallow: /\n'),options);
  const assetUrl=new URL(request.url);assetUrl.pathname=assetPath;
  const response=await env.ASSETS.fetch(new Request(assetUrl,request));
  return protect(response,options);
 }
};
