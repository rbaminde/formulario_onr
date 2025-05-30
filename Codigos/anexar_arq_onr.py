import time
import os
import unidecode
import base64
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException

def carregar_excel():
    caminho = "C:\\Users\\ja.lopes\\Desktop\\dados_formulario devedor.xlsx"
    df = pd.read_excel(caminho)
    return df

def executar_automacao_para_contratos(df):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--kiosk-printing")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    driver.get("https://e-intimacao.onr.org.br/#/login")
    print("chegou: página de login")

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'].form-control"))).send_keys("22007051826")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'].form-control"))).send_keys("Imobjur2025")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ENTRAR')]"))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Pedidos de Intimação')]")))
    print("chegou: login realizado")

    for idx, linha in df.iterrows():
        numero_contrato = str(linha["numero_contrato"]).strip()
        if not numero_contrato or numero_contrato.lower() == "nan":
            print(f"[FIM] Linha {idx+1} vazia. Processo finalizado.")
            break

        print(f"\n=== Iniciando contrato {numero_contrato} ===")
        try:
            executar_automacao(driver, wait, numero_contrato)
        except Exception as e:
            print(f"❌ Erro ao executar contrato {numero_contrato}: {e}")

    driver.quit()
    print("✅ Processo finalizado.")

def executar_automacao(driver, wait, numero_contrato):
    CAMINHO_DEVEDORES = r"Z:\31-EFICIENCIA\JAQUELINE\TESTE DE ENTRADA CRI - ONR"
    CAMINHO_PADRAO = r"Z:\31-EFICIENCIA\JAQUELINE\TESTE DE ENTRADA CRI - ONR\ARQUIVO DE PROCURACAO E SUBSTABELECIMENTO"

    try:
        linha = wait.until(EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{numero_contrato}')]//ancestor::tr")))
    except TimeoutException:
        print(f"❌ Contrato {numero_contrato} não encontrado na página.")
        return

    try:
        checkbox = linha.find_element(By.XPATH, ".//input[@type='checkbox']")
        driver.execute_script("arguments[0].click();", checkbox)
    except ElementNotInteractableException:
        print(f"⚠️ Elemento checkbox não interagível para {numero_contrato}, tentando via JavaScript.")
        driver.execute_script("arguments[0].click();", checkbox)

    try:
        detalhes = linha.find_element(By.XPATH, ".//a[@title='Detalhes']")
        driver.execute_script("arguments[0].click();", detalhes)
    except ElementNotInteractableException:
        print(f"⚠️ Botão 'Detalhes' não interagível, tentando via JavaScript.")
        driver.execute_script("arguments[0].click();", detalhes)

    wait.until(EC.presence_of_element_located((By.ID, "dialog-form-modal-detalhe")))

    bloco_nome = wait.until(EC.presence_of_element_located((By.XPATH, "//b[contains(text(), 'Nome:')]//parent::div")))
    nome_devedor = bloco_nome.text.split("Nome:")[-1].split("Documento")[0].strip()
    nome_devedor_normalizado = unidecode.unidecode(nome_devedor).upper()

    pasta_devedor = os.path.join(CAMINHO_DEVEDORES, nome_devedor_normalizado)
    if not os.path.exists(pasta_devedor):
        print(f"❌ Pasta do devedor '{nome_devedor}' não encontrada.")
        return

    arquivo_proj = os.path.join(pasta_devedor, f"PROJECAO {nome_devedor}.pdf")
    arquivo_req = os.path.join(pasta_devedor, f"REQUERIMENTO {nome_devedor}.pdf")
    if not (os.path.exists(arquivo_proj) and os.path.exists(arquivo_req)):
        print("❌ Arquivos PROJEÇÃO ou REQUERIMENTO não encontrados.")
        return

    arquivos_padrao = [os.path.join(CAMINHO_PADRAO, f) for f in os.listdir(CAMINHO_PADRAO) if f.lower().endswith(".pdf")][:2]

    def anexar_arquivo(caminho):
        input_upload = wait.until(EC.presence_of_element_located((By.ID, "anexar-arquivo")))
        input_upload.send_keys(caminho)
        time.sleep(4)

    anexar_arquivo(arquivo_proj)
    anexar_arquivo(arquivo_req)
    for arq in arquivos_padrao:
        anexar_arquivo(arq)

    try:
        botao_geral = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-display")))
        driver.execute_script("arguments[0].click();", botao_geral)
        time.sleep(1)
    except Exception as e:
        print("❌ Erro ao clicar em 'Geral':", e)

    try:
        botao_detalhar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-circle-info[title='Detalhar']")))
        driver.execute_script("arguments[0].click();", botao_detalhar)
        time.sleep(2)
    except:
        print("⚠️ Botão 'Detalhar' já expandido ou não necessário.")

    try:
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
            "landscape": False,
            "printBackground": True,
            "preferCSSPageSize": True
        })
        with open(os.path.join(pasta_devedor, f"PROTOCOLO {nome_devedor_normalizado}.pdf"), "wb") as f:
            f.write(base64.b64decode(pdf['data']))
        print("✅ PDF salvo.")
    except Exception as e:
        print(f"❌ Erro ao salvar PDF: {e}")

    try:
        icone_fechar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.fa-xmark")))
        driver.execute_script("arguments[0].scrollIntoView(true);", icone_fechar)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", icone_fechar)
    except:
        print("⚠️ Erro ao fechar modal.")

# Executar tudo
df = carregar_excel()
executar_automacao_para_contratos(df)
