# 🎯 RoutineUp

> **Organize seu dia. Transforme sua vida.**

Sistema completo de gestão de rotina e produtividade pessoal, desenvolvido com Flask e design moderno premium.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange.svg)]()

---

## 📋 Índice

- [Sobre](#-sobre)
- [Funcionalidades](#-funcionalidades)
- [Demonstração](#-demonstração)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Capturas de Tela](#-capturas-de-tela)
- [Roadmap](#-roadmap)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 🌟 Sobre

**RoutineUp** é uma aplicação web moderna para gerenciamento de rotinas, tarefas, metas e lembretes. Criado para pessoas que buscam **simplicidade, eficiência e uma experiência visual agradável**.

### Por que RoutineUp?

- ✅ **Interface Premium** - Design moderno com glassmorphism e gradientes
- ✅ **Sistema Inteligente** - Cálculo automático de progresso e prioridades
- ✅ **Dashboard Analítico** - Visualize sua produtividade em tempo real
- ✅ **100% Responsivo** - Funciona perfeitamente em desktop, tablet e mobile
- ✅ **Seguro e Rápido** - Autenticação robusta e performance otimizada

---

## ⚡ Funcionalidades

### 🏠 Dashboard (Hub)
- Visão geral do dia com saudação personalizada
- Timeline de tarefas e lembretes ordenados por horário
- Cards de estatísticas (tarefas concluídas, pendentes, streak)
- Gráficos de produtividade e distribuição por prioridade
- Score de produtividade calculado automaticamente

### ✅ Gestão de Tarefas
- Criação rápida de tarefas com título, descrição e prazo
- Sistema de prioridades (Baixa, Média, Alta)
- Indicadores visuais de status:
  - 🔴 Atrasado
  - 🟡 Hoje
  - 🟣 Em breve
  - 🟢 Futuro
- Filtros inteligentes (Pendentes, Concluídas, Todas)
- Ordenação por prioridade, prazo ou data de criação
- Toggle rápido de conclusão
- Histórico completo com data de conclusão

### 🎯 Sistema de Metas
- **Definição intuitiva**: Valor alvo + unidade (ex: 12 livros, 2000ml)
- **Atualização simplificada**: Informe valores reais, não porcentagens
- **Cálculo automático**: Sistema calcula o progresso (ex: 3/12 = 25%)
- Visualização com anel de progresso animado
- Botão de incremento rápido (+1)
- Barra de progresso com efeito shimmer
- Badges de status (Concluída, Quase lá!)

### 🔔 Lembretes
- Agendamento com data e hora específicas
- Timeline visual com indicadores coloridos
- Status: Visto, Atrasado, Agendado
- Notificações visuais
- Toggle de conclusão

### 👤 Perfil do Usuário
- Upload de foto de perfil (Avatar circular)
- Informações pessoais (Nome, Data de Nascimento, Gênero)
- Alteração segura de senha com validação
- Avatar exibido no topbar

### 🔐 Autenticação Premium
- **Login**: Design split-screen com painel motivacional
- **Cadastro**: Formulário completo com validações
- **Recuperação de Senha**: Sistema de e-mail com token seguro
- **Redefinição**: Medidor de força da senha em tempo real
- Gradientes únicos para cada tela
- Animações suaves e micro-interações

### 💾 Backup e Restauração
- Exportar banco de dados completo
- Importar backup com validação
- Sidebar com acesso rápido

---

## 🎨 Demonstração

### Dashboard Premium
```
┌─────────────────────────────────────────────────────────┐
│  Boa tarde, Diogo! 👋                    Score: 85%     │
│  Terça-feira, 05 de Novembro                            │
│                                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │    5    │  │    2    │  │    0    │  │   25%   │   │
│  │  Hoje   │  │Pendentes│  │  Streak │  │Conclusão│   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
│                                                          │
│  Timeline do Dia:                                       │
│  ⚫ 09:00 - Reunião matinal (Alta)                      │
│  ⚫ 14:00 - Lembrete: Enviar relatório                  │
│  ⚫ 16:30 - Estudar Flask (Média)                       │
└─────────────────────────────────────────────────────────┘
```

### Sistema de Metas
```
┌──────────────────────────────────┐
│  🎯 Ler 12 livros em 2025       │
│                                  │
│          3 / 12 livros           │
│                                  │
│  ▓▓▓▓░░░░░░░░░░░░░░░░  25%      │
│                                  │
│  [+1]  [Editar]                 │
└──────────────────────────────────┘
```

---

## 🛠 Tecnologias

### Backend
- **Python 3.12** - Linguagem principal
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Login** - Gerenciamento de sessões
- **Flask-Migrate** - Migrações de banco
- **Flask-Mail** - Envio de e-mails
- **Werkzeug** - Segurança (hash de senhas)
- **Waitress** - Servidor WSGI para produção

### Frontend
- **HTML5/CSS3** - Estrutura e estilos
- **JavaScript (Vanilla)** - Interatividade
- **Feather Icons** - Biblioteca de ícones
- **Chart.js** - Gráficos de produtividade
- **Recharts** (via CDN) - Visualizações avançadas

### Design System
- **Glassmorphism** - Efeitos de vidro com backdrop-filter
- **Gradientes Dinâmicos** - Cores vibrantes e modernas
- **Animações CSS** - Transições suaves e micro-interações
- **Responsividade** - Mobile-first approach
- **Dark Theme** - Design escuro por padrão

### Banco de Dados
- **SQLite** - Banco de dados local (desenvolvimento)
- **PostgreSQL** - Suporte para produção

---

## 📦 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/routineup.git
cd routineup
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
# Crie um arquivo .env na raiz do projeto
cp .env.example .env

# Edite o .env com suas configurações
```

**Arquivo `.env` exemplo:**
```env
SECRET_KEY=sua-chave-secreta-muito-segura
DATABASE_URL=sqlite:///instance/routine.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app
```

5. **Inicialize o banco de dados**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Execute a aplicação**
```bash
# Desenvolvimento
flask run

# Produção
python app.py
```

7. **Acesse no navegador**
```
http://localhost:5000  (desenvolvimento)
http://localhost:8000  (produção com Waitress)
```

---

## 🚀 Uso

### Criando sua primeira conta

1. Acesse a página inicial
2. Clique em "Cadastre-se gratuitamente"
3. Preencha seus dados
4. Faça login

### Adicionando tarefas

```python
# Método 1: Interface Web
Dashboard → Nova Tarefa → Preencher formulário

# Método 2: Via Python (API futura)
POST /tasks/add
{
  "title": "Estudar Flask",
  "description": "Capítulos 5-7",
  "due_date": "2025-11-10",
  "priority": 1
}
```

### Definindo metas

1. Acesse "Metas" no menu
2. Clique em "Nova Meta"
3. Defina:
   - Título: "Ler 12 livros em 2025"
   - Valor: 12
   - Unidade: livros
4. Atualize o progresso clicando em "+1" ou "Editar"

---

## 📁 Estrutura do Projeto

```
routineup/
│
├── app.py                      # Aplicação principal
├── config.py                   # Configurações
├── requirements.txt            # Dependências
├── .env                        # Variáveis de ambiente (não commitado)
│
├── blueprints/                 # Módulos da aplicação
│   ├── users/                  # Autenticação
│   │   └── routes.py
│   ├── tasks/                  # Gestão de tarefas
│   │   └── routes.py
│   ├── goals/                  # Sistema de metas
│   │   └── routes.py
│   ├── reminders/              # Lembretes
│   │   └── routes.py
│   ├── hub/                    # Dashboard
│   │   └── routes.py
│   ├── profile/                # Perfil do usuário
│   │   └── routes.py
│   └── backup/                 # Backup/Restauro
│       └── routes.py
│
├── models.py                   # Modelos do banco de dados
├── extensions.py               # Extensões Flask (db, login_manager, etc)
│
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── users/                 # Templates de autenticação
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── forgot_password.html
│   │   └── reset_password.html
│   ├── tasks/                 # Templates de tarefas
│   ├── goals/                 # Templates de metas
│   ├── reminders/             # Templates de lembretes
│   ├── hub/                   # Dashboard
│   ├── profile/               # Perfil
│   └── _partials/             # Componentes reutilizáveis
│       └── flash.html
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   ├── app.css            # Estilos principais
│   │   └── theme-pro.css      # Tema premium
│   ├── js/
│   │   ├── theme.js           # Toggle de tema
│   │   └── nav.js             # Navegação/sidebar
│   ├── img/                   # Imagens
│   │   ├── favicon.svg
│   │   └── default-avatar.png
│   └── uploads/               # Arquivos de usuário
│       └── avatars/
│
├── migrations/                 # Migrações do banco
│   └── versions/
│
└── instance/                   # Arquivos locais (não commitados)
    └── routine.db             # Banco SQLite
```

---

## 📸 Capturas de Tela

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Tarefas
![Tarefas](docs/screenshots/tasks.png)

### Metas
![Metas](docs/screenshots/goals.png)

### Login Premium
![Login](docs/screenshots/login.png)

---

## 🗺 Roadmap

### ✅ Concluído
- [x] Sistema de autenticação completo
- [x] CRUD de tarefas com prioridades
- [x] Sistema inteligente de metas
- [x] Dashboard com estatísticas
- [x] Lembretes agendados
- [x] Perfil com avatar
- [x] Backup/Restauração
- [x] Design premium responsivo

### 🚧 Em Desenvolvimento
- [ ] Sistema de notificações push
- [ ] API RESTful completa
- [ ] Modo offline (PWA)
- [ ] Integração com calendário (Google Calendar)
- [ ] Compartilhamento de tarefas
- [ ] Modo claro/escuro alternável

### 🎯 Planejado
- [ ] Aplicativo mobile (React Native)
- [ ] Integrações (Trello, Notion, Todoist)
- [ ] Gamificação (badges, achievements)
- [ ] Relatórios PDF exportáveis
- [ ] Tema customizável pelo usuário
- [ ] Sincronização multi-dispositivo

---

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Siga os passos:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Minha nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões de Código

- **Python**: Seguir PEP 8
- **CSS**: BEM methodology
- **Commits**: Conventional Commits

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Diogo Abreu**

- GitHub: [@diogoabreu](https://github.com/diogoabreu)
- LinkedIn: [Diogo Abreu](https://linkedin.com/in/diogoabreu)
- Email: contato@diogoabreu.dev

---

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Feather Icons](https://feathericons.com/) - Ícones
- [Chart.js](https://www.chartjs.org/) - Gráficos
- Comunidade Python/Flask

---

## 📊 Estatísticas do Projeto

```
├─ Linhas de Código: ~8.000+
├─ Arquivos Python: 15+
├─ Templates HTML: 20+
├─ Rotas: 50+
├─ Modelos: 6
├─ Tempo de Desenvolvimento: 3 meses
└─ Tecnologias: 15+
```

---

<div align="center">

**Feito com ❤️ e ☕ por Diogo Abreu**

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐

[⬆ Voltar ao topo](#-routineup)

</div>