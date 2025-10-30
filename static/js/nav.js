(function(){
  const KEY="sb-collapsed";
  const body=document.body;
  const apply = (v)=> body.classList.toggle("sb-collapsed", v==="1");
  apply(localStorage.getItem(KEY)||"0");
  const btn=document.getElementById("sb-toggle");
  if(btn) btn.addEventListener("click", ()=>{
    const v = body.classList.contains("sb-collapsed") ? "0" : "1";
    localStorage.setItem(KEY, v); apply(v);
  });
})();
(function(){
  const onScroll=()=>document.body.classList.toggle("scrolled", window.scrollY>4);
  onScroll(); window.addEventListener("scroll", onScroll, {passive:true});
})();
