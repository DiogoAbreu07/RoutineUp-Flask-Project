# RoutineUp: Gestor Pessoal de Rotina 🚀

RoutineUp é uma aplicação web completa construída em Flask (Python) para organização pessoal e gestão de rotinas diárias. Este projeto foi desenvolvido como um Trabalho de Conclusão de Curso e inclui um sistema modular para gestão de tarefas, metas, lembretes e perfis de utilizador, bem como um dashboard analítico e notificações por email.

## Funcionalidades Principais

* **Autenticação de Utilizadores:** Sistema completo de registo e login (Flask-Login).
* **Gestão de Tarefas (CRUD):** Criação, edição e exclusão de tarefas com prioridades (Alta, Média, Baixa) e prazos.
* **Gestão de Metas:** Define metas pessoais e acompanha o progresso (0-100%).
* **Gestão de Lembretes:** Agenda lembretes com data e hora específicas.
* **Dashboard (Hub):** Um painel de controlo que mostra estatísticas de produtividade, um gráfico de atividade semanal e uma "timeline" com os eventos do dia.
* **Gestão de Perfil:** Os utilizadores podem atualizar o seu nome, data de nascimento e foto de perfil (com upload de imagens).
* **Backup e Restauro:** Funcionalidade para o utilizador fazer o download e o restauro da sua base de dados SQLite.
* **Alertas de Email:** Um script de fundo (`send_due_date_alerts.py`) que envia emails aos utilizadores quando as suas tarefas têm um prazo próximo (usando Flask-Mail).

## Tecnologias Utilizadas

* **Backend:** Python 3
* **Framework:** Flask
* **Base de Dados:** SQLite
* **ORM:** Flask-SQLAlchemy
* **Migrações:** Flask-Migrate (Alembic)
* **Autenticação:** Flask-Login
* **Notificações:** Flask-Mail
* **Frontend:** HTML5, CSS3, JavaScript (com ícones Feather)
* **Servidor WSGI:** Waitress

---

## 🚀 Instalação e Execução Local

Siga estes passos para executar o projeto no seu computador.

### 1. Pré-requisitos

* Python 3.10+
* Git

### 2. Clonar o Repositório

```bash
git clone [https://github.com/TEU_NOME_DE_UTILIZADOR/routineup.git](https://github.com/TEU_NOME_DE_UTILIZADOR/routineup.git)
cd routineup