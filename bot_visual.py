# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import pyautogui
import time
import mss
import mss.tools
import webbrowser
from datetime import datetime
import os

# Desativa a pausa de segurança do pyautogui (use com cuidado)
pyautogui.FAILSAFE = False

# ===============================
# 📁 CONFIGURAÇÕES GLOBAIS
# ===============================
CONFIGURACOES = {
    "pastas": {
        "assets": "assets",
        "screenshots": "screenshots",
        "logs": "logs"
    },
    "moodle": {
        "url_login": "https://moodle.faat.edu.br/moodle/login/index.php",
        "timeout_login": 20
    },
    "materias": {
        "AnaliseProjeto": "https://moodle.faat.edu.br/moodle/course/view.php?id=6450",
        "Redes": "https://moodle.faat.edu.br/moodle/course/view.php?id=6545",
        "EngenhariaSoftware": "https://moodle.faat.edu.br/moodle/course/view.php?id=6546",
        "IOT": "https://moodle.faat.edu.br/moodle/course/view.php?id=6547",
        "Programacao": "https://moodle.faat.edu.br/moodle/course/view.php?id=6451"
    },
    "automacao": {
        "confianca_imagem": 0.7,
        "confianca_trabalho_final": 0.55,
        "rolagem_por_scroll": -500,
        "tempo_espera_rolagem": 0.4,
        "tempo_espera_abertura_pagina": 5,
        "timeout_esperar_imagem": 10
    },
    "imagens": {
        "botao_acessar": "botao_acessar.png",
        "trabalho_final": "trabalho_final.png",
        "pendente": "pendente.png"
    }
}

# Dicionário para armazenar o status de cada matéria
status_materias = {}

# ===============================
# 🛠️ FUNÇÕES DE APOIO E CONFIGURAÇÃO
# ===============================

def obter_caminho_completo(nome_pasta, nome_arquivo=""):
    """Retorna o caminho completo para uma pasta ou arquivo dentro dela."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, nome_pasta, nome_arquivo)

def criar_pastas_necessarias():
    """Cria as pastas 'assets', 'screenshots' e 'logs' se não existirem."""
    print("🔧 Verificando e criando pastas necessárias...")
    for pasta in CONFIGURACOES["pastas"].values():
        caminho_pasta = obter_caminho_completo(pasta)
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)
            print(f"   📁 Pasta '{caminho_pasta}' criada.")
    print("✅ Pastas verificadas.\n")

def captura_tela(nome_arquivo="debug.png"):
    """Captura a tela inteira do monitor principal e salva como PNG."""
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=nome_arquivo)
    except Exception as e:
        print(f"⚠️ Erro ao capturar a tela: {e}")

def rolar_pagina(total_scrolls=25):
    """Desce a página lentamente usando a rolagem do mouse."""
    print(f"📜 Rolando a página {total_scrolls} vezes para carregar todo o conteúdo...")
    for i in range(total_scrolls):
        pyautogui.scroll(CONFIGURACOES["automacao"]["rolagem_por_scroll"])
        time.sleep(CONFIGURACOES["automacao"]["tempo_espera_rolagem"])
    print("✅ Rolagem concluída.")

def esperar_imagem(caminho_imagem, timeout=10, confianca=0.8):
    """Espera uma imagem aparecer na tela por um determinado tempo."""
    print(f"👀 Aguardando a imagem '{os.path.basename(caminho_imagem)}' aparecer (timeout: {timeout}s)...")
    tempo_inicio = time.time()
    while time.time() - tempo_inicio < timeout:
        try:
            posicao = pyautogui.locateOnScreen(caminho_imagem, confidence=confianca, grayscale=True)
            if posicao:
                print(f"   ✅ Imagem '{os.path.basename(caminho_imagem)}' encontrada!")
                return posicao
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)
    print(f"   ❌ Imagem '{os.path.basename(caminho_imagem)}' NÃO encontrada após {timeout}s.")
    return None

# ===============================
# 🎯 LÓGICA PRINCIPAL DO BOT
# ===============================

def fazer_login_moodle():
    """Abre o Moodle, espera a tela de login e clica no botão de acessar."""
    print("🌐 Abrindo o Moodle no navegador...")
    webbrowser.open(CONFIGURACOES["moodle"]["url_login"])
    
    caminho_botao = obter_caminho_completo(CONFIGURACOES["pastas"]["assets"], CONFIGURACOES["imagens"]["botao_acessar"])
    botao_acessar = esperar_imagem(caminho_botao, timeout=CONFIGURACOES["moodle"]["timeout_login"], confianca=0.6)

    if botao_acessar:
        pyautogui.click(pyautogui.center(botao_acessar))
        print("🚀 Botão 'Acessar' clicado. Login em andamento...")
        time.sleep(CONFIGURACOES["automacao"]["tempo_espera_abertura_pagina"])
        return True
    else:
        print("⚠️ Botão 'Acessar' não encontrado. Verifique se já está logado ou se a página carregou.")
        return False

def verificar_pendencia_na_materia(nome_materia):
    """
    Entra na página da matéria, rola a tela e procura por trabalhos pendentes.
    Retorna um dicionário com o status detalhado da matéria.
    """
    print(f"\n📘 Verificando a matéria: {nome_materia}")
    url_materia = CONFIGURACOES["materias"][nome_materia]
    webbrowser.open(url_materia)
    time.sleep(CONFIGURACOES["automacao"]["tempo_espera_abertura_pagina"])

    rolar_pagina()
    
    caminho_screenshot = obter_caminho_completo(CONFIGURACOES["pastas"]["screenshots"], f"tela_{nome_materia}.png")
    captura_tela(caminho_screenshot)

    status_materia = {
        "nome": nome_materia,
        "trabalho_encontrado": False,
        "pendente": False,
        "observacao": ""
    }

    try:
        caminho_trabalho = obter_caminho_completo(CONFIGURACOES["pastas"]["assets"], CONFIGURACOES["imagens"]["trabalho_final"])
        trabalho_posicao = pyautogui.locateOnScreen(caminho_trabalho, confidence=CONFIGURACOES["automacao"]["confianca_trabalho_final"], grayscale=True)
    except pyautogui.ImageNotFoundException:
        print(f"   ⚠️ Imagem 'trabalho_final.png' não foi encontrada na tela de {nome_materia}.")
        trabalho_posicao = None
        status_materia["observacao"] = "Trabalho final não encontrado"

    if trabalho_posicao:
        print("   📘 'Trabalho Final' encontrado. Verificando status...")
        status_materia["trabalho_encontrado"] = True
        
        regiao_para_procurar = (
            trabalho_posicao.left + trabalho_posicao.width,
            trabalho_posicao.top - 20,
            300,
            trabalho_posicao.height + 40
        )
        
        try:
            caminho_pendente = obter_caminho_completo(CONFIGURACOES["pastas"]["assets"], CONFIGURACOES["imagens"]["pendente"])
            pendente_posicao = pyautogui.locateOnScreen(caminho_pendente, region=regiao_para_procurar, confidence=CONFIGURACOES["automacao"]["confianca_imagem"], grayscale=True)
        except pyautogui.ImageNotFoundException:
            print("   🟣 Status 'Pendente' não encontrado próximo ao trabalho.")
            pendente_posicao = None

        if pendente_posicao:
            print("   🟢 Status 'Pendente' encontrado!")
            status_materia["pendente"] = True
            caminho_screenshot_pendente = obter_caminho_completo(CONFIGURACOES["pastas"]["screenshots"], f"pendente_{nome_materia}.png")
            captura_tela(caminho_screenshot_pendente)
            print(f"   📸 Screenshot da pendência salvo em '{caminho_screenshot_pendente}'")
            status_materia["observacao"] = "Trabalho final com status PENDENTE"
        else:
            print("   🟣 Trabalho encontrado, mas o status NÃO é 'Pendente'.")
            status_materia["observacao"] = "Trabalho final encontrado, mas sem pendência"
    else:
        print(f"   ✅ Nenhum 'Trabalho Final' encontrado para {nome_materia}.")
        status_materia["observacao"] = "Nenhum trabalho final encontrado"

    return status_materia

def voltar_pagina_inicial():
    """Volta para a página anterior usando o atalho do navegador."""
    print("↩️ Voltando para a página anterior...")
    pyautogui.hotkey('alt', 'left')
    time.sleep(3)

def gerar_relatorio_final():
    """Gera e salva o relatório final das pendências no console e em um arquivo."""
    print("\n" + "="*50)
    print("📊 RELATÓRIO FINAL DE PENDÊNCIAS")
    print("="*50)
    
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Coletar matérias com pendências
    materias_com_pendencia = [materia for materia, status in status_materias.items() if status["pendente"]]
    materias_sem_trabalho = [materia for materia, status in status_materias.items() if not status["trabalho_encontrado"]]
    materias_em_dia = [materia for materia, status in status_materias.items() if status["trabalho_encontrado"] and not status["pendente"]]

    # Relatório no console
    print(f"📅 Relatório gerado em: {data_hora}")
    print(f"📚 Total de matérias verificadas: {len(status_materias)}")
    print(f"⚠️  Matérias com pendências: {len(materias_com_pendencia)}")
    print(f"✅ Matérias em dia: {len(materias_em_dia)}")
    print(f"🔍 Matérias sem trabalho final: {len(materias_sem_trabalho)}")
    
    if materias_com_pendencia:
        print("\n❌ MATÉRIAS COM PENDÊNCIAS:")
        for materia in materias_com_pendencia:
            print(f"   🔸 {materia} - {status_materias[materia]['observacao']}")
    
    if materias_em_dia:
        print("\n✅ MATÉRIAS EM DIA:")
        for materia in materias_em_dia:
            print(f"   🟢 {materia} - {status_materias[materia]['observacao']}")
    
    if materias_sem_trabalho:
        print("\n🔍 MATÉRIAS SEM TRABALHO FINAL:")
        for materia in materias_sem_trabalho:
            print(f"   🔎 {materia} - {status_materias[materia]['observacao']}")

    print(f"\n📷 Prints das telas salvas na pasta 'screenshots'.")

    # Relatório em arquivo
    relatorio_texto = "="*50 + "\n"
    relatorio_texto += "RELATÓRIO DE PENDÊNCIAS - BOT MOODLE\n"
    relatorio_texto += "="*50 + "\n"
    relatorio_texto += f"Data e hora: {data_hora}\n"
    relatorio_texto += f"Total de matérias verificadas: {len(status_materias)}\n"
    relatorio_texto += f"Matérias com pendências: {len(materias_com_pendencia)}\n"
    relatorio_texto += f"Matérias em dia: {len(materias_em_dia)}\n"
    relatorio_texto += f"Matérias sem trabalho final: {len(materias_sem_trabalho)}\n\n"
    
    if materias_com_pendencia:
        relatorio_texto += "MATÉRIAS COM PENDÊNCIAS:\n"
        for materia in materias_com_pendencia:
            relatorio_texto += f"❌ {materia} - {status_materias[materia]['observacao']}\n"
        relatorio_texto += "\n"
    
    if materias_em_dia:
        relatorio_texto += "MATÉRIAS EM DIA:\n"
        for materia in materias_em_dia:
            relatorio_texto += f"✅ {materia} - {status_materias[materia]['observacao']}\n"
        relatorio_texto += "\n"
    
    if materias_sem_trabalho:
        relatorio_texto += "MATÉRIAS SEM TRABALHO FINAL:\n"
        for materia in materias_sem_trabalho:
            relatorio_texto += f"🔍 {materia} - {status_materias[materia]['observacao']}\n"
    
    relatorio_texto += "\n" + "="*50 + "\n\n"

    caminho_log = obter_caminho_completo(CONFIGURACOES["pastas"]["logs"], f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(caminho_log, "w", encoding="utf-8") as f:
        f.write(relatorio_texto)
    
    print(f"📁 Relatório salvo em: '{caminho_log}'")
    print("="*50)

# ===============================
# 🚀 EXECUÇÃO PRINCIPAL DO SCRIPT
# ===============================

if __name__ == "__main__":
    try:
        print("🧠 Iniciando o bot do Moodle — versão com relatório detalhado 🚀\n")
        
        criar_pastas_necessarias()
        
        fazer_login_moodle()
        
        # Loop principal para verificar cada matéria
        for nome_materia in CONFIGURACOES["materias"].keys():
            status = verificar_pendencia_na_materia(nome_materia)
            status_materias[nome_materia] = status
            voltar_pagina_inicial()

        gerar_relatorio_final()
        
        print("\n🏁 Bot finalizado com sucesso!")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado durante a execução do bot: {e}")
        print("🔍 Tentando gerar um relatório parcial com as informações coletadas até o momento...")
        try:
            gerar_relatorio_final()
        except Exception as e_rel:
            print(f"❌ Não foi possível gerar o relatório: {e_rel}")
        print("🏁 Bot finalizado com erros.")