function toggle(el, inputId){
  const i = document.getElementById(inputId);
  if(!i) return;
  i.type = (i.type === "password" ? "text" : "password");
  el.textContent = (i.type === "password" ? "Mostrar" : "Ocultar");
}

function strengthMeter(pwd){
  const bar = document.querySelectorAll(".strength span");
  bar.forEach(b=>b.className="");
  if(!pwd) return;

  let score = 0;
  if(pwd.length >= 8) score++;
  if(/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) score++;
  if(/\d/.test(pwd)) score++;
  if(/[^A-Za-z0-9]/.test(pwd)) score++;

  const classes = ["weak","fair","good","strong"];
  for(let i=0;i<Math.min(score,4);i++){
    bar[i].classList.add("on", classes[Math.max(0,score-1)]);
  }
}

document.addEventListener("click", (e)=>{
  const t = e.target;
  if(t.matches("[data-toggle]")){
    e.preventDefault();
    toggle(t, t.getAttribute("data-toggle"));
  }
});

document.addEventListener("input", (e)=>{
  if(e.target.matches("#reg_password")){
    strengthMeter(e.target.value);
  }
});
