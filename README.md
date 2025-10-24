# 🤖 Moodle Bot — Automação Inteligente de Tarefas no Moodle

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

---

## 🧠 Sobre o Projeto

O **Moodle Bot** é uma ferramenta de **automação completa para o Moodle**, desenvolvida em **Python**, projetada para executar tarefas repetitivas de forma autônoma.  
Ele utiliza **PyAutoGUI**, **OpenCV** e **Selenium** para controlar o navegador e interagir com a interface do Moodle — como um usuário humano, mas muito mais rápido ⚡.

Ideal para quem quer:
- Automatizar logins e navegação;
- Coletar informações e relatórios;
- Baixar e enviar arquivos;
- Gerar logs e relatórios diários.

---

## 🚀 Funcionalidades Principais

✅ Login automático no Moodle  
✅ Acesso a cursos e atividades  
✅ Download e upload de arquivos  
✅ Extração de relatórios e notas  
✅ Execução em loop (agendada ou contínua)  
✅ Logs automáticos e tratamento de erros  
✅ Integração com variáveis de ambiente para segurança  

---

## 🧩 Tecnologias Utilizadas

| Tecnologia | Função |
|-------------|--------|
| **Python 3.11+** | Linguagem base do projeto |
| **PyAutoGUI** | Automação visual (mouse e teclado) |
| **OpenCV** | Reconhecimento de imagem (ícones, botões) |
| **Selenium** | Automação web (login e scraping) |
| **BeautifulSoup / Requests** | Coleta e parsing de dados |
| **dotenv** | Gerenciamento de variáveis de ambiente |
| **logging / time / os** | Controle e monitoramento da execução |

---

## 📁 Estrutura de Pastas

```
moodle_bot/
│
├── bot_visual.py          # Script principal
├── credentials.env        # Credenciais do Moodle (usuário, senha, URL)
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
│
├── assets/                # Ícones e imagens usados pelo PyAutoGUI
│   ├── chrome_task.png
│   ├── moodle_icon.png
│   └── ...
│
├── logs/                  # Logs automáticos de execução
│   ├── 2025-10-24.log
│   └── ...
│
└── utils/                 # (Opcional) Funções auxiliares
    ├── browser.py
    ├── image_tools.py
    └── scheduler.py
```

---

## ⚙️ Instalação

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seuusuario/moodle-bot.git
cd moodle-bot
```

### 2️⃣ Criar o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/macOS
```

### 3️⃣ Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variáveis de ambiente
Crie um arquivo chamado `.env` ou `credentials.env` com o conteúdo:

```
MOODLE_USER=seu_usuario
MOODLE_PASS=sua_senha
MOODLE_URL=https://seudominio.moodle.com
```

---

## ▶️ Execução

### Rodar o bot manualmente
```bash
python bot_visual.py
```

### Rodar o bot em loop (modo autônomo)
```bash
python bot_visual.py --loop
```

### Agendar execução diária (Windows)
Crie um arquivo `.bat`:
```bat
@echo off
cd C:\caminho\para\moodle_bot
call venv\Scripts\activate
python bot_visual.py
```
E agende no **Agendador de Tarefas do Windows**.

---

## 🪄 Logs e Monitoramento

Os logs são salvos automaticamente na pasta `logs/`, com o formato:
```
logs/2025-10-24.log
```

Cada execução registra:
- Horário de início e fim  
- Ações executadas  
- Erros detectados  
- Tempo total de execução  

Exemplo:
```
[2025-10-24 09:42:12] ✅ Login realizado com sucesso
[2025-10-24 09:42:18] 📂 Entrando no curso "Automação Avançada"
[2025-10-24 09:42:45] ⬇️ Download concluído: atividade1.pdf
```

---

## 💡 Dicas de Uso

🔹 Mantenha a resolução de tela fixa (ex: 1920x1080).  
🔹 Certifique-se de que o tema e idioma do Chrome sejam iguais aos das imagens da pasta `assets/`.  
🔹 Teste as coordenadas e ícones após cada atualização do Moodle.  
🔹 Use `pyautogui.sleep()` para ajustar tempo entre cliques se notar falhas.  

---

## 🧰 Futuras Implementações

- [ ] Painel gráfico interativo (dashboard com métricas e status)
- [ ] Interface para configuração de cursos e tarefas
- [ ] Suporte multiplataforma completo (Windows/Linux)
- [ ] Integração com Telegram/Discord para notificações
- [ ] API REST para automação remota

---

## 🧑‍💻 Autor

**Desenvolvido por [José Luiz](https://github.com/zzin742)**  
💬 _"Automatizar é libertar tempo para o que realmente importa."_  

---

## 📜 Licença

Distribuído sob a licença **MIT**.  
Veja o arquivo `LICENSE` para mais detalhes.

---

## ⭐ Contribua

Se este projeto te ajudou, considere:
- Dar uma ⭐ no repositório  
- Reportar bugs e sugerir melhorias  
- Compartilhar com a comunidade acadêmica e devs

---

### ⚡ _Feito com Python, café e pura automação._
