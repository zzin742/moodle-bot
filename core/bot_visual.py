# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import time
import shutil
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# ===============================
# ⚙️ CONFIGURAÇÕES GERAIS
# ===============================
load_dotenv()

CONFIGURACOES = {
    "pastas": {
        "logs": "logs",
        "screenshots": "screenshots",
    },
    "moodle": {
        "url_login": os.getenv("MOODLE_URL"),
        "timeout_login": 20
    },
    "materias": {
        "AnaliseProjeto": "https://moodle.faat.edu.br/moodle/course/view.php?id=6450",
        "Redes": "https://moodle.faat.edu.br/moodle/course/view.php?id=6545",
        "EngenhariaSoftware": "https://moodle.faat.edu.br/moodle/course/view.php?id=6546",
        "IOT": "https://moodle.faat.edu.br/moodle/course/view.php?id=6547",
        "Programacao": "https://moodle.faat.edu.br/moodle/course/view.php?id=6451"
    }
}

status_materias = {}

# ===============================
# 🧠 FUNÇÕES DE SUPORTE
# ===============================

def obter_caminho_completo(nome_pasta, nome_arquivo=""):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, nome_pasta, nome_arquivo)

def criar_pastas():
    for pasta in CONFIGURACOES["pastas"].values():
        os.makedirs(obter_caminho_completo(pasta), exist_ok=True)

def captura_tela(driver, nome_arquivo):
    """Salva screenshot direto do Selenium."""
    caminho = obter_caminho_completo(CONFIGURACOES["pastas"]["screenshots"], nome_arquivo)
    driver.save_screenshot(caminho)
    print(f"📸 Screenshot salvo em {caminho}")

# ===============================
# 🌐 LOGIN SELENIUM
# ===============================

def iniciar_driver():
    """Inicia o Chrome com perfil temporário isolado para evitar cache e travamentos."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    user_data_dir = os.path.join(os.getcwd(), "chrome_temp_profile")
    os.makedirs(user_data_dir, exist_ok=True)
    options.add_argument(f"--user-data-dir={user_data_dir}")

    print(f"🚀 Iniciando Chrome com perfil temporário em: {user_data_dir}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver, user_data_dir

def fazer_login(driver):
    print("🌐 Acessando página de login do Moodle...")
    driver.get(CONFIGURACOES["moodle"]["url_login"])
    time.sleep(3)

    usuario = os.getenv("MOODLE_USER")
    senha = os.getenv("MOODLE_PASS")

    if not usuario or not senha:
        print("❌ Credenciais não encontradas no arquivo .env.")
        return False

    try:
        campo_user = driver.find_element(By.ID, "username")
        campo_pass = driver.find_element(By.ID, "password")
        botao_login = driver.find_element(By.ID, "loginbtn")

        campo_user.send_keys(usuario)
        campo_pass.send_keys(senha)
        botao_login.click()

        WebDriverWait(driver, 15).until(
            EC.any_of(
                EC.url_contains("dashboard"),
                EC.url_contains("my")
            )
        )

        print("✅ Login realizado com sucesso!")
        return True
    except Exception as e:
        print(f"⚠️ Aviso: possível problema no login ({e}) — continuando mesmo assim.")
        return True

# ===============================
# 🔍 VERIFICAR PENDÊNCIAS REAIS (ROBUSTO)
# ===============================

def _safe_text(el):
    """Retorna o texto em minúsculas de um elemento (ou '' se None)."""
    if el is None:
        return ""
    try:
        return el.get_text(" ", strip=True).lower()
    except Exception:
        return ""

def _has_any(text, keywords):
    """True se qualquer palavra-chave aparece no texto (case-insensitive)."""
    t = (text or "").lower()
    return any(k.lower() in t for k in keywords)

def verificar_materia(driver, nome_materia, url_materia):
    """
    Abre a matéria, rola toda a página, captura screenshot e
    detecta pendências olhando títulos e badges/labels de status.
    Evita lambdas de class_ que geravam NoneType errors.
    """
    print(f"\n📘 Verificando matéria: {nome_materia}")
    status = {"trabalho_encontrado": False, "pendente": False, "observacao": ""}

    try:
        driver.get(url_materia)

        # Espera um contêiner típico de conteúdo do curso
        try:
            WebDriverWait(driver, 12).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".course-content, #region-main, .format-tiles, .format-topics")
                )
            )
        except Exception:
            # Segue mesmo assim; alguns temas demoram a sinalizar
            pass

        # Rola até o fim para carregar todo conteúdo dinâmico
        last_h = driver.execute_script("return document.body.scrollHeight")
        for _ in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.1)
            new_h = driver.execute_script("return document.body.scrollHeight")
            if new_h == last_h:
                break
            last_h = new_h

        # Volta pro topo (print mais útil)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.3)

        # Screenshot final da página já carregada
        caminho_png = f"tela_{nome_materia}.png"
        captura_tela(driver, caminho_png)

        # Parse seguro
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Seleciona atividades de forma previsível (sem lambda no class_)
        atividades = soup.select("li.activity, div.activity")
        if not atividades:
            # Alternativas comuns de temas
            atividades = soup.select(".activityinstance, .assign, .modtype_assign, .activityitem")

        if not atividades:
            status["observacao"] = "Nenhuma atividade detectada"
            print(f"🔍 {nome_materia}: sem atividades visíveis.")
            return status

        pendentes = 0
        entregues = 0
        vistos = 0

        # Palavras-chave de status (ajuste conforme seu tema)
        KW_PENDENTE = ["pendente", "não enviado", "nao enviado", "não entregue", "nao entregue", "aguardando envio", "não enviado ainda", "atrasado"]
        KW_ENTREGUE = ["enviado", "entregue", "concluído", "concluido", "em dia", "feito", "submetido", "enviada"]

        for bloco in atividades:
            vistos += 1

            # Texto amplo do bloco
            texto = _safe_text(bloco)

            # Coleta badges/status labels comuns em vários temas
            badges = []
            for sel in [".badge", ".badge-status", ".status", ".submissionstatus", ".label", ".activity-status"]:
                for b in bloco.select(sel):
                    t = _safe_text(b)
                    if t:
                        badges.append(t)

            texto_status = " ".join(filter(None, [texto] + badges)).lower()

            if _has_any(texto_status, KW_PENDENTE):
                pendentes += 1
            elif _has_any(texto_status, KW_ENTREGUE):
                entregues += 1
            else:
                # Heurísticas por classes conhecidas (sem 'in None')
                cls = bloco.get("class") or []
                cls_join = " ".join(cls).lower()
                if _has_any(cls_join, ["notattempted", "submissionnotgraded", "overdue"]):
                    pendentes += 1
                elif _has_any(cls_join, ["completed", "submissionstatussubmitted", "submitted"]):
                    entregues += 1

        if pendentes > 0:
            status.update({
                "trabalho_encontrado": True,
                "pendente": True,
                "observacao": f"{pendentes} pendência(s) detectada(s) em {vistos} atividade(s) visível(is)"
            })
            print(f"❌ {nome_materia}: {pendentes} pendência(s) ({vistos} atividades analisadas).")
        elif entregues > 0:
            status.update({
                "trabalho_encontrado": True,
                "pendente": False,
                "observacao": f"{entregues} tarefa(s) entregue(s) em {vistos} atividade(s)"
            })
            print(f"✅ {nome_materia}: em dia ({entregues} entregues, {vistos} atividades).")
        else:
            status["observacao"] = f"Sem status identificado (analisadas {vistos} atividades)"
            print(f"🟣 {nome_materia}: sem status claro ({vistos} atividades).")

        return status

    except Exception as e:
        print(f"❌ Erro ao processar {nome_materia}: {e}")
        status["observacao"] = f"Erro ({e})"
        return status


# ===============================
# 📊 RELATÓRIO FINAL
# ===============================

def gerar_relatorio():
    caminho_log = obter_caminho_completo("logs", f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print("\n" + "="*50)
    print("📊 RELATÓRIO FINAL DE PENDÊNCIAS")
    print("="*50)
    print(f"📅 Gerado em: {data_hora}")
    print(f"📚 Total de matérias verificadas: {len(status_materias)}")

    with open(caminho_log, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO MOODLE BOT - {data_hora}\n")
        f.write("="*60 + "\n")
        for m, s in status_materias.items():
            simbolo = "❌" if s["pendente"] else "✅" if s["trabalho_encontrado"] else "🔍"
            f.write(f"{simbolo} {m} - {s['observacao']}\n")

    print(f"📁 Relatório salvo em: {caminho_log}")
    print("="*50)

# ===============================
# 🚀 EXECUÇÃO PRINCIPAL
# ===============================

if __name__ == "__main__":
    criar_pastas()
    driver, profile_path = iniciar_driver()

    try:
        if not fazer_login(driver):
            print("❌ Falha no login. Encerrando.")
            driver.quit()
            exit()

        for nome, url in CONFIGURACOES["materias"].items():
            status_materias[nome] = verificar_materia(driver, nome, url)

        gerar_relatorio()
        print("\n🏁 Bot finalizado com sucesso!")

    finally:
        driver.quit()
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path, ignore_errors=True)
            print("🧹 Perfil temporário do Chrome removido.")
        print("\n📊 Para abrir o painel:")
        print("   python -m streamlit run dashboard/app.py")
