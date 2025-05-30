from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

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
    numero_cartorio = str(linha["num_cartorio"]).strip()
    if "-" in numero_cartorio:
        digito_verificador_contrato = numero_cartorio.split(" - ")[-1].strip
    else:
        digito_verificador_contrato = 0
    driver.find_element(By.XPATH, '//label[contains(text(), "DV Contrato")]/following::input[1]').send_keys(digito_verificador_contrato)
    

def data_assinatura(driver, linha):
    wait = WebDriverWait(driver, 15)
    data_assinatura = str(linha["data_ass"])
    driver.find_element(By.XPATH, "//label[contains(text(), 'Data Assinatura')]/following::input[1]").send_keys(str(linha["data_ass"]))
    


def estado(driver,linha):
    wait = WebDriverWait(driver, 15)
    Select(driver.find_element(By.XPATH, "//label[contains(text(), 'Estado')]/following::select[1]")).select_by_value(str(linha["estado_corresp1"]))
    estado_corresp = str(linha["estado_corresp1"])

def municipio(driver,linha):
    wait = WebDriverWait(driver, 15)
    Select(driver.find_element(By.XPATH, "//label[contains(text(), 'Município')]/following::select[1]")).select_by_value(str(linha["cidade1"]))
    cidade = str(linha["cidade1"])


def matricula(driver,linha):
    wait = WebDriverWait(driver, 15)
    driver.find_element(By.XPATH, '//label[contains(text(), "Matrículas")]/following::input[1]').send_keys(str(linha['matricula']))

def endereço_imovel(driver,linha):
    wait = WebDriverWait(driver, 15)
    driver.find_element(By.XPATH, "//label[contains(text(), 'Endereço do Imóvel')]/following::input[1]").send_keys(str(linha["tipo_end_imovel"] + " " + str(linha['endereco_imovel']) + " " + str(linha['numero_imovel']) ))
    tipo_end_imovel = str(linha["tipo_end_imovel"] + " " + str(linha['endereco_imovel']) + " " + str(linha['numero_imovel']) )