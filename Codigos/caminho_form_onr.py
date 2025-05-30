# Bibliotecas usadas
import os
import pandas as pd
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import filedialog
import sys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tela_inicial import clicar_botoes_iniciais
from formulario_credor import preencher_nome_credor
from preencher_requerimento import selecionar_tipo_contrato, contrato_financiamento, digito_verificador_contrato,matricula, endereço_imovel, data_assinatura, estado, municipio


def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_PROJETO = get_base_path()
# Caminhos relativos
driver_path = os.path.join(PASTA_PROJETO, "Navegador", "chromedriver.exe")
# Janela oculta só para abrir o seletor de arquivos
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
file_path = filedialog.askopenfilename(
    title="Selecione o Excel com os dados do formulário",
    filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
)

if not file_path:
    print("[ERRO] Nenhum arquivo selecionado. Encerrando...")
    exit()

df = pd.read_excel(file_path)

# Dados fixos do credor
usuario = '220.070.518-26'
senha = 'Imobjur2025'

# Inicializa o driver com as opções configuradas 

driver = webdriver.Chrome(service=Service(driver_path))
    # Aqui vai o fluxo para estados ONR
wait = WebDriverWait(driver, 10)
driver.get('https://e-intimacao.onr.org.br/#/login')
driver.maximize_window()
try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Permitir cookies')]"))
        ).click()
        print("Cookies permitidos com sucesso")
except:
        print("Cookies já estavam aceitos")

time.sleep(1)

try:
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div/div/div/div[1]/div[2]/form/div[2]/button[2]'))).click()
        print('Botão para preencher login pressionado')
except:
        print('Botão não foi pressionado')

inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.form-control")))

    # Preenche o primeiro input com o CPF
inputs[0].send_keys(usuario)

    # Preenche o segundo input com a senha
inputs[1].send_keys(senha)

    
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div/div/div/div[1]/div[2]/form/div[3]/button[1]"))).click()

for _, linha in df.iterrows():
    clicar_botoes_iniciais(driver)
    selecionar_tipo_contrato(driver)
    contrato_financiamento(driver, linha)
    digito_verificador_contrato(driver,linha)
    data_assinatura(driver, linha)
   # municipio(driver,linha)
    estado(driver,linha)
    matricula(driver, linha)
    endereço_imovel(driver,linha)
    preencher_nome_credor(driver)

fechar = input("Deseja fechar o navegador? (s/n): ")
if fechar.lower() == "s":
    driver.quit()