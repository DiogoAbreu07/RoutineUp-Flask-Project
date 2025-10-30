(function(){
  const KEY="rup-theme";
  const root=document.documentElement;
  const sys = matchMedia("(prefers-color-scheme: dark)").matches ? "dark":"light";
  function apply(t){ document.body.setAttribute("data-theme", t); localStorage.setItem(KEY,t); }
  apply(localStorage.getItem(KEY) || sys);
  const btn=document.getElementById("theme-toggle");
  if(btn) btn.addEventListener("click", ()=>{
    const cur=document.body.getAttribute("data-theme")||"dark";
    apply(cur==="dark"?"light":"dark");
  });
})();
