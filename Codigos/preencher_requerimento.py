from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time



def selecionar_tipo_contrato(driver):
    wait = WebDriverWait(driver, 15)
    Select(driver.find_element(By.XPATH, '//label[contains(text(), "Tipo de Contrato")]/following::select[1]')).select_by_value("HABITACIONAL_PROPRIOS")

def contrato_financiamento(driver, linha):
    wait = WebDriverWait(driver, 15)
    driver.find_element(By.XPATH, '//label[contains(text(), "Contrato")]/following::input[1]').send_keys(str(linha["numero_contrato"]))
    numero_cartorio = int(linha["num_cartorio"])

def digito_verificador_contrato(driver,linha):
    wait = WebDriverWait(driver, 15)
    driver.find_element(By.XPATH, '//label[contains(text(), "DV Contrato")]/following::input[1]').send_keys(str(linha["numero_contrato"]))
    numero_cartorio = int(linha["num_cartorio"])

def matricula(driver,linha):
    wait = WebDriverWait(driver, 15)
    driver.find_element(By.XPATH, '//label[contains(text(), "Matrículas")]/following::input[1]').send_keys(str(linha['matricula']))
