// JS app
// abrir externos em nova aba
document.querySelectorAll('a[href^="http"]').forEach(a=>{
  const loc = location.hostname;
  if(!a.href.includes(loc)) a.target = "_blank";
});

// rolagem suave para âncoras internas
document.querySelectorAll('a[href^="#"]').forEach(a=>{
  a.addEventListener('click', e=>{
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if(el){ e.preventDefault(); el.scrollIntoView({behavior:'smooth', block:'start'}); }
  });
});
