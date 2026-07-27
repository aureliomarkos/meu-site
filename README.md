# MarkosDev Backend

Backend FastAPI + SQLAlchemy para o portfólio MarkosDev — inclui formulário de contato, blog/notícias, sistema de clientes com mensagens, chat com IA (OpenRouter) e painel administrativo.

## Funcionalidades

- **Contato** — formulário público que envia mensagens para o banco
- **Notícias / Blog** — CRUD completo com painel admin e seed automático
- **Clientes** — registro, login e sistema de mensagens entre cliente e admin
- **Chat com IA** — assistente virtual "MarkosBot" via OpenRouter (streaming SSE)
- **Painel Admin** — gerencia notícias e mensagens dos clientes (autenticação por senha)
- **Frontend estático** — páginas HTML/CSS/JS servidas pelo FastAPI (`/page/`, `/mobile/`)
- **Banco SQLite** (padrão) — pode ser trocado para PostgreSQL/MySQL via `DATABASE_URL`
- **Logs** — registro de tentativas de cadastro de clientes em `logs/`

## Estrutura

```
meu-site/
├── app/
│   ├── __init__.py
│   ├── main.py           # aplicação FastAPI, CORS, static files, routers
│   ├── config.py         # configurações via .env (pydantic-settings)
│   ├── database.py       # engine, sessão e base declarativa
│   ├── models.py         # modelos SQLAlchemy (ContactMessage, Client, ClientMessage, News)
│   ├── schemas.py        # schemas Pydantic (request / response)
│   ├── crud.py           # operações no banco
│   ├── seed.py           # seed automático de notícias de exemplo
│   ├── page/             # frontend estático desktop
│   │   ├── index.html
│   │   ├── script.js
│   │   └── styles.css
│   └── routes/
│       ├── __init__.py
│       ├── admin.py      # /api/admin/* — painel administrativo
│       ├── chat.py       # /api/chat    — chat com IA (OpenRouter)
│       ├── client_messages.py  # /api/clients/{id}/messages/*
│       ├── clients.py    # /api/clients/* — registro e login
│       ├── contact.py    # /api/contact/* — formulário de contato
│       └── news.py       # /api/news/* — listagem pública de notícias
├── logs/                 # logs de cadastro de clientes
├── mobile/               # frontend estático mobile
├── tests/
│   └── test_clients.py
├── requirements.txt
└── README.md
```

## Instalação

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///./markosdev.db
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
ADMIN_PASSWORD=sua_senha_admin
OPENROUTER_API_KEY=sua_chave_openrouter
OPENROUTER_MODEL=modelo_de_ia
```

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DATABASE_URL` | String de conexão do banco | `sqlite:///./markosdev.db` |
| `CORS_ORIGINS` | Origens permitidas (separadas por vírgula) | `*` |
| `ADMIN_PASSWORD` | Senha do painel administrativo | *(vazio)* |
| `OPENROUTER_API_KEY` | Chave da API OpenRouter (chat IA) | *(vazio)* |
| `OPENROUTER_MODEL` | Modelo de IA no OpenRouter | *(vazio)* |

## Execução

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse a documentação interativa em: http://localhost:8000/docs

Na primeira execução, o banco é criado automaticamente e um seed de notícias de exemplo é populado.

## Endpoints

### Contato

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/contact` | Enviar mensagem de contato |
| `GET` | `/api/contact` | Listar mensagens de contato |

### Notícias (público)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/news` | Listar notícias ativas |
| `GET` | `/api/news/count` | Contar notícias ativas |
| `GET` | `/api/news/{id}` | Obter notícia por ID |

### Clientes

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/clients` | Registrar novo cliente |
| `POST` | `/api/clients/login` | Login do cliente |

### Mensagens do Cliente

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/clients/{id}/messages` | Criar mensagem |
| `GET` | `/api/clients/{id}/messages` | Listar mensagens do cliente |
| `PUT` | `/api/clients/{id}/messages/{msg_id}` | Atualizar mensagem |
| `DELETE` | `/api/clients/{id}/messages/{msg_id}` | Remover mensagem |

### Chat IA

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/chat` | Enviar mensagem ao MarkosBot (streaming SSE) |

### Admin (requer header `x-admin-password`)

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/admin/login` | Autenticar admin |
| `GET` | `/api/admin/news` | Listar todas as notícias |
| `GET` | `/api/admin/news/{id}` | Obter notícia por ID |
| `POST` | `/api/admin/news` | Criar notícia |
| `PUT` | `/api/admin/news/{id}` | Atualizar notícia |
| `DELETE` | `/api/admin/news/{id}` | Excluir notícia |
| `GET` | `/api/admin/client-messages` | Listar todas as mensagens de clientes |
| `PUT` | `/api/admin/client-messages/{id}` | Atualizar mensagem de cliente (resposta/status) |

## Tecnologias

- **FastAPI** — framework web async
- **SQLAlchemy 2.0** — ORM
- **Pydantic / pydantic-settings** — validação e configuração
- **SQLite** (padrão) / PostgreSQL (produção)
- **OpenRouter API** — integração com IA para chat
- **httpx** — cliente HTTP async (streaming)

