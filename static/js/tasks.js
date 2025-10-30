(function(){
  const KEY = "sb-collapsed"; // Chave no localStorage
  const body = document.body; // Alvo é o body

  // Função para aplicar/remover a classe do body
  const apply = (v) => {
    body.classList.toggle("sb-collapsed", v === "1");
  };

  // Aplica o estado guardado ou o padrão (0 = aberto)
  apply(localStorage.getItem(KEY) || "0");

  // Encontra o botão de toggle
  const btn = document.getElementById("sb-toggle");

  // Adiciona o evento de clique ao botão
  if (btn) {
    btn.addEventListener("click", () => {
      // Verifica o estado atual e inverte
      const currentState = body.classList.contains("sb-collapsed");
      const newState = currentState ? "0" : "1"; // Se está colapsado (true), novo estado é '0' (aberto)

      // Guarda o novo estado e aplica a classe
      localStorage.setItem(KEY, newState);
      apply(newState);
    });
  }

  // Lógica para adicionar a classe 'scrolled' ao body quando rolar a página
  // (Mantida, útil para efeitos no topbar se necessário)
  const onScroll = () => {
    // Verifica se o main-content-wrapper está a ser rolado
    const mainContent = document.querySelector('.main-content-wrapper');
    if (mainContent) {
      body.classList.toggle("scrolled", mainContent.scrollTop > 4);
    }
  };
  
  // Adiciona o listener ao main-content-wrapper
  const mainContent = document.querySelector('.main-content-wrapper');
  if (mainContent) {
      onScroll(); // Verifica no carregamento
      mainContent.addEventListener("scroll", onScroll, { passive: true });
  }

})();