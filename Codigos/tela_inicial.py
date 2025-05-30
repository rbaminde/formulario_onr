from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tkinter import messagebox

def clicar_botoes_iniciais(driver):
    wait = WebDriverWait(driver, 10)

    try:
        checkbox = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//label[contains(., 'Estou ciente.')]/input")
        ))
        time.sleep(0.5)
        checkbox.click()
    except:
        messagebox.INFO("Erro", "Erro ao clicar no botão 'Eu concordo'")

    try:
        botao_cadastrar = driver.find_element(By.XPATH, "//button[@title='Cadastrar Pedidos']")
        botao_cadastrar.click()
    except:
        messagebox.INFO("Erro", "Erro ao clicar no botão 'Cadastrar Pedidos'")