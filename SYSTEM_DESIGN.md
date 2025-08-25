# Interview Bot - System Design

## Diagrama de Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                INTERVIEW BOT SYSTEM                             │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   👤 USUÁRIO    │    │  🌐 FRONTEND    │    │ 📱 WHATSAPP     │
│                 │    │   (React)       │    │    USERS        │
│  • Cadastro     │    │                 │    │                 │
│  • Formulário   │    │  • Landing Page │    │ • Recebe msgs   │
│                 │    │  • Registro     │    │ • Envia resps   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │ HTTP POST            │ HTTP                 │ WhatsApp
          │ /api/users/register  │                      │ Messages
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 FASTAPI BACKEND                                   │
│                         (Nossa Aplicação Principal)                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   📡 WEBHOOKS   │  │  👥 USER API    │  │  ⏰ SCHEDULER   │                │
│  │                 │  │                 │  │                 │                │
│  │ • Recebe msgs   │  │ • Registro      │  │ • APScheduler   │                │
│  │ • Processa STOP │  │ • Unsubscribe   │  │ • Envio diário  │                │
│  │ • Salva resps   │  │ • CRUD users    │  │ • 9h da manhã   │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
│           │                     │                     │                        │
│           │                     │                     │                        │
│           └─────────────────────┼─────────────────────┘                        │
│                                 │                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                        🧠 BUSINESS LOGIC                               │  │
│  │                                                                         │  │
│  │  • Seleção de perguntas por área técnica                              │  │
│  │  • Análise de respostas com IA                                        │  │
│  │  • Geração de feedback personalizado                                  │  │
│  │  • Controle de frequência (1 pergunta/dia)                           │  │
│  │  • Suporte multi-idioma (PT, EN, ES)                                 │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                 │                                              │
└─────────────────────────────────┼──────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            🗄️ DATA LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │   📊 SQLite     │  │  📝 QUESTIONS   │  │  💬 RESPONSES   │                │
│  │   DATABASE      │  │     BANK        │  │    HISTORY      │                │
│  │                 │  │                 │  │                 │                │
│  │ • users         │  │ • JavaScript    │  │ • user_id       │                │
│  │ • questions     │  │ • Python        │  │ • question_id   │                │
│  │ • responses     │  │ • Ruby          │  │ • response_text │                │
│  │                 │  │ • DSA           │  │ • ai_feedback   │                │
│  │                 │  │ • Multi-lang    │  │ • score (1-10)  │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         🌐 EXTERNAL SERVICES                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │  📱 WhatsApp    │  │  🤖 OpenAI      │  │  🔧 ngrok       │                │
│  │  Cloud API      │  │     API         │  │  (dev only)     │                │
│  │                 │  │                 │  │                 │                │
│  │ • Send msgs     │  │ • GPT-4         │  │ • Tunnel local  │                │
│  │ • Receive msgs  │  │ • Response      │  │ • Public URL    │                │
│  │ • Media support │  │   analysis      │  │ • Webhook test  │                │
│  │ • Status updates│  │ • Feedback gen  │  │                 │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘

## Fluxo de Dados - Casos de Uso

### 📝 CASO 1: Registro de Usuário
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ User    │───▶│Frontend │───▶│FastAPI  │───▶│Database │
│fills    │    │validates│    │creates  │    │stores   │
│form     │    │data     │    │user     │    │user     │
└─────────┘    └─────────┘    └─────────┘    └─────────┘

### ⏰ CASO 2: Envio Diário de Pergunta
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│Scheduler│───▶│Business │───▶│WhatsApp │───▶│User's   │
│triggers │    │Logic    │    │API      │    │Phone    │
│9AM      │    │selects Q│    │sends msg│    │receives │
└─────────┘    └─────────┘    └─────────┘    └─────────┘

### 💬 CASO 3: Resposta do Usuário
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│User     │───▶│WhatsApp │───▶│Webhook  │───▶│OpenAI   │───▶│Response │
│answers  │    │Cloud API│    │receives │    │analyzes │    │sent back│
│question │    │forwards │    │processes│    │generates│    │to user  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘

### 🛑 CASO 4: Comando STOP
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│User     │───▶│WhatsApp │───▶│Webhook  │───▶│Database │
│sends    │    │forwards │    │detects  │    │marks    │
│"STOP"   │    │message  │    │STOP cmd │    │inactive │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

## Componentes Detalhados

### 🚀 FastAPI Backend (Core)

**Responsabilidades:**

- Gerenciar webhooks do WhatsApp
- Processar registro de usuários
- Agendar envio de perguntas
- Integrar com IA para análise
- Gerenciar estado dos usuários

**Endpoints principais:**

- `GET /webhook/whatsapp` - Verificação do webhook
- `POST /webhook/whatsapp` - Receber mensagens
- `POST /api/users/register` - Registro de usuários
- `GET /health` - Health check

### 🗄️ Database Layer (SQLite)

**Tabelas:**

- **users**: Dados dos usuários registrados
- **questions**: Banco de perguntas técnicas
- **user_responses**: Histórico de respostas e feedback

**Relacionamentos:**

- User 1:N UserResponse
- Question 1:N UserResponse

### 📱 WhatsApp Integration

**Fluxos:**

- **Outbound**: Sistema → WhatsApp API → Usuário
- **Inbound**: Usuário → WhatsApp API → Webhook → Sistema

### 🤖 AI Integration (OpenAI)

**Funcionalidades:**

- Análise de qualidade das respostas
- Geração de feedback personalizado
- Sugestões de melhoria
- Scoring (1-10)

### ⏰ Task Scheduling

**APScheduler:**

- Execução diária às 9h
- Seleção de usuários ativos
- Envio de perguntas personalizadas
- Controle de frequência

## Escalabilidade e Melhorias Futuras

### 📈 Para Crescimento:

1. **Database**: SQLite → PostgreSQL
2. **Cache**: Redis para sessões
3. **Queue**: Celery para tasks assíncronas
4. **Monitoring**: Logs estruturados
5. **Deploy**: Docker + Cloud (AWS/GCP)

### 🔒 Segurança:

- Rate limiting nos endpoints
- Validação de tokens WhatsApp
- Sanitização de inputs
- Backup automático do banco

### 🌍 Internacionalização:

- Suporte a mais idiomas
- Timezone por usuário
- Perguntas localizadas
