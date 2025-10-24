import sys
sys.stdout.reconfigure(encoding='utf-8')

import pyautogui
import time
import mss
import mss.tools
import webbrowser
from datetime import datetime
import os

print("🧠 Iniciando o bot do Moodle — versão relatório diário 🚀")

# ===============================
# 📁 CONFIGURAÇÃO DE PASTAS
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

def caminho(nome):
    """Retorna o caminho completo do arquivo dentro de /assets"""
    return os.path.join(ASSETS, nome)

# ===============================
# 🎯 CONFIGURAÇÃO DAS MATÉRIAS
# ===============================
materias = {
    "AnaliseProjeto": "https://moodle.faat.edu.br/moodle/course/view.php?id=6450",
    "Redes": "https://moodle.faat.edu.br/moodle/course/view.php?id=6545",
    "EngenhariaSoftware": "https://moodle.faat.edu.br/moodle/course/view.php?id=6546",
    "IOT": "https://moodle.faat.edu.br/moodle/course/view.php?id=6547",
    "Programacao": "https://moodle.faat.edu.br/moodle/course/view.php?id=6451"
}

pendencias = []  # lista para guardar matérias com tarefas pendentes

# ===============================
# 📸 FUNÇÕES DE APOIO
# ===============================

def captura(nome="debug.png"):
    """Captura a tela (sem tela preta)"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=nome)

def rolar_pagina(total_scrolls=25):
    """Desce lentamente a página inteira"""
    for i in range(total_scrolls):
        pyautogui.scroll(-500)
        time.sleep(0.4)

def procurar_trabalho():
    """Procura trabalho final e verifica se está pendente"""
    for tentativa in range(5):
        try:
            print(f"🔍 Tentando localizar trabalho final (tentativa {tentativa+1})...")
            trabalho = pyautogui.locateOnScreen(caminho('trabalho_final.png'), confidence=0.55, grayscale=True)
            if trabalho:
                print("📘 Trabalho Final encontrado! Verificando se está pendente...")
                pendente = pyautogui.locateOnScreen(caminho('pendente.png'), confidence=0.7, grayscale=True)
                if pendente:
                    print("🟢 Trabalho pendente encontrado!")
                    pyautogui.moveTo(pyautogui.center(trabalho))
                    time.sleep(1)
                    return True
                else:
                    print("🟣 Trabalho encontrado, mas não está pendente.")
                    return False
            else:
                pyautogui.scroll(-800)
                time.sleep(1)
        except pyautogui.ImageNotFoundException:
            print("⚠️ Imagem não encontrada nessa rolagem, tentando novamente...")
            pyautogui.scroll(-800)
            time.sleep(1)
    return False

# ===============================
# 🌐 LOGIN E ABERTURA DO MOODLE
# ===============================
moodle_url = "https://moodle.faat.edu.br/moodle/login/index.php"
print("🔎 Procurando ícone do Chrome na barra de tarefas...")

icone = pyautogui.locateOnScreen(caminho('chrome_task.png'), confidence=0.8)

if icone:
    print("✅ Chrome encontrado! Clicando...")
    pyautogui.click(pyautogui.center(icone))
    time.sleep(2)

    print("⌨️ Digitando o endereço do Moodle...")
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite(moodle_url)
    pyautogui.press('enter')
    time.sleep(6)

    botao = pyautogui.locateOnScreen(caminho('botao_acessar.png'), confidence=0.6, grayscale=True)
    if botao:
        pyautogui.click(pyautogui.center(botao))
        print("🚀 Login realizado com sucesso!")
        time.sleep(6)
    else:
        print("⚠️ Já parece estar logado.")

    # ===============================
    # 📚 LOOP NAS MATÉRIAS
    # ===============================
    for nome, url in materias.items():
        print(f"\n📘 Entrando na matéria: {nome}")
        webbrowser.open(url)
        time.sleep(7)

        print("📜 Descendo a página para verificar tarefas...")
        rolar_pagina(25)
        captura(f"screenshots/tela_{nome}.png")

        encontrou = procurar_trabalho()

        if encontrou:
            pendencias.append(nome)
            captura(f"screenshots/pendente_{nome}.png")
            print(f"📸 Screenshot salva como screenshots/pendente_{nome}.png")
        else:
            print(f"✅ Nenhum trabalho pendente encontrado em {nome}.")

        print("↩️ Voltando para a página inicial...")
        pyautogui.hotkey('alt', 'left')
        time.sleep(5)

    # ===============================
    # 🧾 RELATÓRIO FINAL
    # ===============================
    print("\n📊 RELATÓRIO FINAL:")
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if pendencias:
        print("⚠️ As seguintes matérias têm tarefas pendentes:")
        for materia in pendencias:
            print(f"   🔸 {materia}")
        print("\n📷 Foram salvos prints das telas das pendências.")

        with open("logs/relatorio_pendencias.txt", "a", encoding="utf-8") as f:
            f.write(f"\n📅 {data}\n")
            f.write("⚠️ Matérias com pendências:\n")
            for materia in pendencias:
                f.write(f"   🔸 {materia}\n")
            f.write("-" * 30 + "\n")

    else:
        print("✅ Todas as matérias estão em dia! Nenhuma pendência encontrada.")
        with open("logs/relatorio_pendencias.txt", "a", encoding="utf-8") as f:
            f.write(f"\n📅 {data} — Nenhuma pendência encontrada.\n")
            f.write("-" * 30 + "\n")

    print("\n📁 Relatório salvo em: logs/relatorio_pendencias.txt")

else:
    print("❌ Ícone do Chrome não encontrado.")
