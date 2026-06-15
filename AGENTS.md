# Manual do Agente de IA (AGENTS.md)

## Projeto: Agendador de Posts para Redes Sociais

---

> [!IMPORTANT]
> Este documento serve como guia de contexto, arquitetura e padrões de codificação para agentes de IA que atuarão no desenvolvimento deste projeto. Leia-o atentamente antes de criar ou modificar qualquer arquivo.

---

## 1. Visão Geral da Arquitetura do Sistema

O sistema é baseado no framework **Django** no backend com um frontend renderizado no servidor usando **Bootstrap 5** para estilização e **jQuery** para interações assíncronas (AJAX). O banco de dados é o **Neon (PostgreSQL Serverless)**.

```
                   +---------------------------------------+
                   |          Navegador do Usuário         |
                   |      (HTML5 / Bootstrap 5 / jQuery)   |
                   +-------------------+---------------+---+
                                       |               ^
                         Chamadas AJAX |               | Páginas Renderizadas
                         & Form HTML   |               | (Django Templates)
                                       v               |
                   +-------------------+---------------+---+
                   |             Backend Django            |
                   | (Views, ORM, Forms, OAuth Connectors) |
                   +-----+-------------+-------------+-----+
                         |             |             |
       Leitura/Escrita   |             | Agendamento | Executa
       de Dados          |             | de Tarefas  | Tarefas
                         v             v             v
  +----------------------+---+   +-----+-------------+-----+
  | Banco de Dados Neon      |   | Motor de Tarefas        |
  | (PostgreSQL Serverless)  |   | (Django Q2)             |
  +--------------------------+   +-------------+-----------+
                                               |
                                               | Requisições HTTP
                                               v
                                 +-------------+-----------+
                                 | APIs das Redes Sociais  |
                                 | (FB, IG, LinkedIn, X)   |
                                 +-------------------------+
```

---

## 2. Padrões de Projeto e Diretrizes de Código

Para garantir a consistência e a manutenibilidade do código, os agentes de IA devem seguir estritamente as regras abaixo:

### 2.1. Backend (Django)
*   **Identificadores Únicos (UUID):** Todas as tabelas do banco de dados devem usar `UUIDField` como chave primária (`id`) em vez de números inteiros sequenciais (evita exposição de IDs na URL e previne conflitos ao usar database branching no Neon).
*   **Separação de Conceitos (Services Layer):**
    *   **Models:** Devem conter apenas definições de campos, propriedades simples e métodos de persistência direta.
    *   **Views:** Devem lidar exclusivamente com o fluxo HTTP (validação de formulários, renderização de templates ou retorno de JSON).
    *   **Services / Connectors:** Toda a lógica de integração com APIs externas (OAuth, postagem de conteúdo, upload de mídia) deve residir em classes de serviço isoladas na pasta `integrations/connectors/`.
*   **Gerenciamento de Configurações:** Nunca insira credenciais, chaves de API ou segredos diretamente no código. Utilize o arquivo `.env` e a biblioteca `python-environ` ou `python-dotenv`.

### 2.2. Banco de Dados (Neon)
*   Escreva sempre migrações limpas e reversíveis.
*   Utilize o tipo `JSONB` no PostgreSQL (via `models.JSONField` no Django) para armazenar metadados flexíveis de mídias e respostas de APIs externas.

### 2.3. Frontend (Bootstrap & jQuery)
*   **Sem Frameworks SPA:** Não utilize React, Vue ou Angular. O frontend deve usar Django Templates (`.html`) herdando de um `base.html` comum.
*   **Requisições AJAX:**
    *   Todas as requisições AJAX do jQuery devem incluir o cabeçalho CSRF do Django:
        ```javascript
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
        ```
    *   Sempre forneça feedback visual de "carregando" (spinners do Bootstrap) e manipulação amigável de erros em caso de falha nas chamadas.
*   **Calendário:** Utilize a biblioteca **FullCalendar v6** (via CDN) integrada via jQuery para implementar o calendário interativo de publicações.

---

## 3. Estrutura de Diretórios Recomendada

O projeto Django deve ser organizado utilizando a seguinte estrutura modular de aplicações:

```
social_scheduler/
│
├── manage.py
├── .env.example
├── .gitignore
│
├── social_scheduler/            # Configurações globais do projeto Django
│   ├── __init__.py
│   ├── settings.py              # Configuração de Neon, Django Q2, etc.
│   ├── urls.py                  # Roteamento global
│   └── wsgi.py
│
├── accounts/                    # Gerenciamento de Usuários e Workspace
│   ├── models.py                # CustomUser, Organization
│   ├── views.py                 # Login, Cadastro, Perfil
│   ├── urls.py
│   └── forms.py
│
├── scheduler/                   # Núcleo de Postagem e Agendamento
│   ├── models.py                # Post, ScheduledPost
│   ├── views.py                 # CRUD de Posts, JSON do Calendário
│   ├── urls.py
│   ├── tasks.py                 # Funções disparadas pelo Django Q2
│   └── forms.py
│
├── integrations/                # Integração com Redes Sociais (OAuth & APIs)
│   ├── models.py                # SocialAccount
│   ├── urls.py                  # Callbacks de OAuth
│   ├── views.py
│   └── connectors/              # Serviços de comunicação externa
│       ├── base.py              # Classe abstrata BaseSocialConnector
│       ├── facebook.py
│       ├── instagram.py
│       ├── linkedin.py
│       └── twitter.py
│
├── logs/                        # Logs de Auditoria
│   ├── models.py                # AuditLog
│   └── middleware.py            # Middleware para interceptar ações do usuário
│
├── notifications/               # Sistema de Notificações
│   ├── models.py                # Notification
│   └── services.py              # Envio de Notificações (in-app, email)
│
├── static/                      # Arquivos estáticos globais
│   ├── css/
│   │   └── custom.css           # Estilos personalizados e polimento visual
│   └── js/
│       ├── calendar.js          # Lógica do FullCalendar + jQuery
│       └── main.js
│
└── templates/                   # Templates HTML globais
    ├── base.html                # Layout principal com Navbar, Sidebar e Toast de notificações
    ├── accounts/
    ├── core/                    # Dashboard inicial
    └── scheduler/
```

---

## 4. Estrutura de Segurança de Tokens (Crítico)

Para atender aos requisitos de segurança do PRD:
1.  **Criptografia de Tokens:** Ao salvar tokens de acesso (`access_token` e `refresh_token`) em `SocialAccount`, utilize uma biblioteca de criptografia simétrica (ex: `cryptography.fernet`).
2.  **Chave de Criptografia:** A chave de criptografia deve ser armazenada no `.env` (`SOCIAL_ENCRYPTION_KEY`) e nunca commitada no repositório.
3.  **Exemplo de Implementação Conceitual:**
    ```python
    from cryptography.fernet import Fernet
    from django.conf import settings

    def get_cipher():
        return Fernet(settings.SOCIAL_ENCRYPTION_KEY.encode())

    def encrypt_token(token: str) -> str:
        cipher = get_cipher()
        return cipher.encrypt(token.encode()).decode()

    def decrypt_token(encrypted_token: str) -> str:
        cipher = get_cipher()
        return cipher.decrypt(encrypted_token.encode()).decode()
    ```

---

## 5. Roteiro de Implementação Passo a Passo (AI Agent Roadmap)

Os agentes de IA devem focar nas tarefas seguindo a ordem abaixo. Cada etapa deve incluir testes unitários.

### Fase 1: Setup do Ambiente e Estrutura Inicial
*   [ ] Criar ambiente virtual Python e instalar dependências (`django`, `django-environ`, `psycopg2-binary`, `django-q2`, `cryptography`).
*   [ ] Configurar conexão com o Neon PostgreSQL no `settings.py`.
*   [ ] Criar as aplicações Django: `accounts`, `scheduler`, `integrations`, `logs` e `notifications`.
*   [ ] Configurar o modelo de usuário customizado (`CustomUser`) e a entidade `Organization`.

### Fase 2: Autenticação e Gestão de Organizações
*   [ ] Implementar telas de cadastro (Signup) e login baseadas em Bootstrap 5.
*   [ ] Criar lógica para que o primeiro usuário crie uma `Organization`, e novos usuários possam ser convidados por administradores.
*   [ ] Configurar controle de acesso básico (RBAC) com os papéis `Admin`, `Manager` e `Creator`.

### Fase 3: Conexões de Rede Social (Framework de Integração)
*   [ ] Criar o modelo `SocialAccount` com campos criptografados.
*   [ ] Implementar a classe abstrata `BaseSocialConnector` em `integrations/connectors/base.py`.
*   [ ] Desenvolver mocks para fluxos de OAuth 2.0 e rotas de callback das redes sociais para viabilizar testes offline antes da integração real.

### Fase 4: Criação e Validação de Posts
*   [ ] Criar o modelo `Post` e o formulário de criação.
*   [ ] Desenvolver a interface de composição de posts usando Bootstrap (com contador de caracteres JS dinâmico por rede social e preview em tempo real).
*   [ ] Implementar upload assíncrono de mídias salvando-as localmente (para desenvolvimento) ou em um bucket S3/Cloudinary compatível, registrando as referências em formato JSONB no modelo `Post`.

### Fase 5: Agendamento e Calendário
*   [ ] Implementar o modelo `ScheduledPost` relacionando posts às redes sociais de destino e datas futuras.
*   [ ] Criar tela do Calendário utilizando **FullCalendar v6** e **jQuery AJAX** para buscar, mover (arrastar e soltar) e editar agendamentos diretamente na visualização do calendário.
*   [ ] Implementar as views para listagem do Histórico de Publicações com paginação e filtros.

### Fase 6: Motor de Agendamento (Background Worker)
*   [ ] Configurar o **Django Q2** no projeto utilizando a tabela do banco de dados como broker (evitando a necessidade de Redis em ambientes serverless simples).
*   [ ] Criar a tarefa periódica `scheduler.tasks.publish_due_posts` programada para rodar a cada 1 minuto.
*   [ ] Desenvolver a lógica de publicação assíncrona, descriptografia de tokens, tratamento de erros das APIs, política de retentativas e transição correta de status do post.

### Fase 7: Dashboard, Logs e Notificações
*   [ ] Criar o Dashboard inicial com gráficos de volume de postagens usando **Chart.js** e contadores de status de posts.
*   [ ] Criar middleware para gravação automática de `AuditLog` para ações críticas.
*   [ ] Implementar painel de notificações in-app (dropdown na navbar via jQuery) e despacho de e-mails para falhas de agendamento.

---

## 6. Comandos Úteis e Validação

Para validar o funcionamento do projeto durante o desenvolvimento, utilize os seguintes comandos no terminal:

*   **Executar Migrações:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
*   **Iniciar o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
*   **Iniciar o Worker do Django Q2:**
    ```bash
    python manage.py qcluster
    ```
*   **Rodar os Testes Unitários:**
    ```bash
    python manage.py test
    ```
---

