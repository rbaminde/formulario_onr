from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time

nome_credor = "BANCO SANTANDER (BRASIL) S.A."
Qualificação = "BANCO SANTANDER (BRASIL) S.A., instituição financeira devidamente autorizada a funcionar pelo Banco Central do Brasil, sediada à Avenida Presidente Juscelino Kubitschek, 2041/2235, Vila Nova Conceição, CEP 04543-011, inscrita no CNPJ sob nº 90.400.888/0001-42"
CNPJ = "90.400.888/0001-42"
def preencher_nome_credor(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((
            By.XPATH, '//label[contains(text(), "Nome do Credor")]/following::input[1]'
        ))).send_keys(nome_credor)
    wait.until(EC.presence_of_element_located((
            By.XPATH, '//label[contains(text(), "CNPJ do Credor")]/following::input[1]'
        ))).send_keys(CNPJ)
    wait.until(EC.presence_of_element_located((
            By.XPATH, '//label[contains(text(), "Qualificação completa do credor")]/following::textarea[1]'
        ))).send_keys(Qualificação)
   
