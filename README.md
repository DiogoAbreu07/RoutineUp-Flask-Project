# RoutineUp: Gestor Pessoal de Rotina 🚀

<div>
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0%2B-red?style=for-the-badge&logo=sqlalchemy" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite" alt="SQLite">
</div>

Aplicação web completa para gestão de rotina e produtividade, desenvolvida em Flask. O projeto implementa um sistema modular para gestão de tarefas, metas e lembretes, com autenticação de utilizadores e um dashboard analítico. Este projeto foi originalmente desenvolvido como um Trabalho de Conclusão de Curso.

##  Status do Projeto

✅ **Projeto Concluído (Versão 1.0)**

---

## 🚀 Funcionalidades (Features)

* **✅ Autenticação de Utilizadores:** Sistema completo de registo e login (usando Flask-Login).
* **✅ Gestão de Tarefas (CRUD):** Criação, edição e exclusão de tarefas com prioridades (Alta, Média, Baixa) e prazos.
* **✅ Gestão de Metas:** Define metas pessoais e acompanha o progresso (0-100%).
* **✅ Gestão de Lembretes:** Agenda lembretes com data e hora específicas.
* **✅ Dashboard (Hub):** Um painel de controlo central que mostra:
    * Estatísticas de produtividade (tarefas concluídas, streak, etc.).
    * Gráfico de atividade semanal.
    * Uma "timeline" com os eventos e tarefas do dia.
* **✅ Gestão de Perfil:** Os utilizadores podem atualizar o seu nome, data de nascimento e foto de perfil (com upload de imagens).
* **✅ Backup e Restauro:** Funcionalidade para o utilizador fazer o download e o restauro da sua base de dados SQLite.
* **✅ Alertas de Email:** Um script de fundo (`send_due_date_alerts.py`) que envia emails aos utilizadores quando as suas tarefas têm um prazo próximo (usando Flask-Mail).

---

## 🔧 Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework:** Flask
* **Servidor WSGI:** Waitress
* **Banco de Dados:** SQLite
* **ORM:** SQLAlchemy (com Flask-SQLAlchemy)
* **Migrações de BD:** Alembic (com Flask-Migrate)
* **Autenticação:** Flask-Login
* **Envio de Email:** Flask-Mail
* **Frontend:** HTML5, CSS3, JavaScript
* **Ícones:** Feather Icons

---
## 🚀 Instalação e Execução Local

## ▶️ Como Executar o Projeto

Siga os passos abaixo para executar o projeto localmente:

### 1. Pré-requisitos

* Python 3.10+
* Git

### 2. Clonar o Repositório:

```bash
git clone [https://github.com/TEU_NOME_DE_UTILIZADOR/routineup.git](https://github.com/TEU_NOME_DE_UTILIZADOR/routineup.git)
cd routineup
