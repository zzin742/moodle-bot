# 🤖 Moodle Bot — Automação Inteligente + Dashboard Interativo

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-ativo-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Interface](https://img.shields.io/badge/UI-Streamlit-red)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

---

## 🧠 Sobre o Projeto

O **Moodle Bot** é uma ferramenta de **automação visual e monitoramento inteligente** para o Moodle, desenvolvida em **Python**.  
Ele combina **PyAutoGUI**, **OpenCV** e **Streamlit** para automatizar tarefas e exibir resultados em tempo real através de um **painel gráfico interativo**.

💡 O bot acessa automaticamente o Moodle, percorre as matérias, identifica pendências e gera relatórios detalhados — tudo isso enquanto você toma um café ☕.

---

## 🚀 Principais Funcionalidades

### 🤖 Automação Moodle
✅ Login automático no Moodle  
✅ Acesso a cursos e atividades  
✅ Verificação de pendências e trabalhos finais  
✅ Captura automática de screenshots  
✅ Geração de relatórios TXT organizados por data  
✅ Logs automáticos e controle de execução  

### 📊 Dashboard Interativo
✅ Painel visual com métricas em tempo real (Streamlit)  
✅ Gráficos dinâmicos (barras, pizza, linha do tempo)  
✅ Filtros por data, matéria e status  
✅ Busca por palavra-chave  
✅ Download dos relatórios filtrados em CSV  
✅ Atualização automática a cada nova execução  

### ⚙️ Extras
✅ Abertura automática do painel após execução do bot  
✅ Compatibilidade total com Windows e Linux  
✅ Código modular, limpo e otimizado  
✅ Logs e erros tratados com mensagens claras  

---

## 🧩 Tecnologias Utilizadas

| Tecnologia | Função |
|-------------|--------|
| **Python 3.11+** | Linguagem base |
| **PyAutoGUI** | Automação visual (mouse, teclado e captura de tela) |
| **OpenCV** | Reconhecimento de elementos na tela |
| **mss** | Captura de telas (screenshots automáticos) |
| **Streamlit** | Interface do dashboard |
| **Plotly** | Criação de gráficos interativos |
| **dotenv / os / sys** | Configuração e ambiente |
| **Subprocess** | Execução automática do painel Streamlit |

---

## 📁 Estrutura de Pastas

```
moodle-bot/
│
├── core/
│   ├── bot_visual.py        # Script principal de automação (bot)
│   └── assets/              # Ícones e imagens usados pelo bot
│
├── dashboard/
│   └── app.py               # Dashboard interativo com Streamlit
│
├── logs/                    # Relatórios automáticos em texto
│   └── relatorio_20251028_132725.txt
│
├── screenshots/             # Capturas automáticas de tela
│
├── requirements.txt         # Dependências do projeto
└── README.md                # Este arquivo
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

---

## ▶️ Execução

### Modo automático (recomendado)
Execute o bot — ao finalizar, o painel abrirá automaticamente:
```bash
python core/bot_visual.py
```

> ✅ O Moodle Bot fará todo o processo de login, checagem de matérias e geração de relatório.  
> Ao finalizar, ele abrirá automaticamente o painel gráfico no navegador.

### Modo manual (somente dashboard)
Se quiser apenas abrir o painel:
```bash
python -m streamlit run dashboard/app.py
```

---

## 🪄 Dashboard Interativo

📊 Após a execução, o painel exibe:
- Total de matérias monitoradas  
- Quantas estão “Em dia”, “Pendentes” ou “Sem trabalho”  
- Linha do tempo da evolução dos status  
- Tabela filtrável com todos os detalhes  

*(adicione aqui um print do painel quando quiser mostrar no GitHub)*

---

## 💡 Dicas de Uso

🔹 Use sempre a mesma resolução de tela (ex: 1920x1080).  
🔹 Mantenha o tema e idioma do navegador iguais às imagens da pasta `assets/`.  
🔹 Certifique-se de que o Chrome esteja aberto e sem pop-ups bloqueando a automação.  
🔹 Evite movimentar o mouse durante a execução do bot.  

---

## 🧰 Futuras Implementações

- [ ] Interface de configuração de cursos e parâmetros direto no dashboard  
- [ ] Integração com Telegram/Discord para notificações automáticas  
- [ ] API REST para controle remoto (FastAPI)  
- [ ] Exportação automática dos relatórios em PDF  
- [ ] Monitoramento contínuo em tempo real  

---

## 🆕 Atualizações Recentes (v2.0 — Outubro/2025)

### 🚀 Melhorias no Bot (`core/bot_visual.py`)
- **Abertura automática do painel Streamlit:**  
  O bot agora abre o dashboard no navegador automaticamente após gerar o relatório.  
- **Código otimizado:**  
  Funções reorganizadas e redundâncias removidas, mantendo todas as funcionalidades originais.  
- **Relatórios padronizados:**  
  Relatórios com nomes uniformes (`relatorio_YYYYMMDD_HHMMSS.txt`) e estrutura de dados limpa.  
- **Logs aprimorados:**  
  Saídas mais detalhadas no console, com identificação de pendências e status de cada matéria.  
- **Melhor compatibilidade entre Windows e Linux.**

### 📊 Melhorias no Dashboard (`dashboard/app.py`)
- **Painel gráfico completo com Streamlit + Plotly:**  
  Exibe gráficos interativos (barras, pizza, linha do tempo) com filtros e métricas.  
- **Leitura automática de relatórios:**  
  Detecta arquivos de log automaticamente e organiza os dados por data.  
- **Filtros avançados e busca textual:**  
  Permite filtrar por período, matéria e status, além de busca por palavra-chave.  
- **Download de relatórios filtrados (CSV).**  
- **Cache com expiração automática (5 minutos)** para maior performance.

### 🧠 Outros Melhoramentos
- Execução mais estável e modular.  
- Estrutura de pastas reorganizada e documentada.  
- Código pronto para expansão futura (API, notificações, etc).  

---

## 🧑‍💻 Autor

**Desenvolvido por [José Luiz](https://github.com/zzin742)**  
💬 _"Automatizar é transformar tempo em liberdade."_  

---

## 📜 Licença

Distribuído sob a licença **MIT**.  
Consulte o arquivo `LICENSE` para mais detalhes.

---

## ⭐ Contribua

Se este projeto te ajudou:
- 🌟 Dê uma estrela no repositório  
- 🐛 Reporte bugs ou sugira melhorias  
- 📣 Compartilhe com outros devs e estudantes  

---

### ⚡ _Feito com Python, Streamlit e um toque de automação._ 🚀
