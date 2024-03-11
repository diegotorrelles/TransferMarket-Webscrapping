from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

#driver de selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # para esperar los elementos en selenium
from selenium.webdriver.support import expected_conditions as ec # para condiciones en selenium
from selenium.common.exceptions import TimeoutException # excepcion de timeout en selenium 
from selenium.webdriver.common.keys import Keys #para pulsar teclas especiales rollo avanzar pagina


import time
import pickle #para guardar/cargar las cookies
import os
import sys

driver_manager = ChromeDriverManager() #Añadiriamos log level para tener una terminal mas vacia

chromedriver_path = driver_manager.install()
#print(chromedriver_path)
options = Options()
user_agent = "Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

options.add_argument(f"user-agent={user_agent}") # define un user agent personalizado
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled") #Importante para que piense que no somos un bot
options.add_argument("--disable-popup-blocking") #quita los pop ups creo
options.add_argument("--disable-password-manager-reauthentication")
options.add_argument("--accept-all-cookies")

#options.add_argument("--headless") # con esto no te habre la ventana 

#### PARAMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER

exp_opt = [
    "enable-automation", #para que no muestre la notificacion de un softaware de prueba
    "ignore-certificate-errors",
    "enable-logging" # para que no te ponga lo del dev tools
]  

options.add_experimental_option("excludeSwitches",exp_opt)

service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service,options=options)
wait = WebDriverWait(driver,15) # tiempo de espera hasta que el elemento este disponible

print("antes de entrar en la pagina")

driver.get("https://www.transfermarkt.es/")

print("ANTES DE PILLAR EL ELEMENTPO")



iframe = driver.find_element(By.CSS_SELECTOR, "iframe#sp_message_iframe_1015264")

driver.switch_to.frame(iframe)


cookies = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,"button.message-component.message-button.no-children.focusable.accept-all.sp_choice_type_11.first-focusable-el"))) 
#cookies = driver.find_element(By.CSS_SELECTOR,"button.message-component")
cookies.click()

driver.switch_to.default_content()

barra = driver.find_element(By.CSS_SELECTOR,"ul.main-navbar__container")
valoresBarra = barra.find_elements(By.CSS_SELECTOR,"li")

elemento = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//span[starts-with(@id, 'ASTAGQ_plc_close_')]")))     ### Para quitar la publi
elemento.click()

valoresDeMercadoSpan = valoresBarra[2].find_element(By.CSS_SELECTOR,"span").click()         ### Click de Valores de Mercado

elemento = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a.main-navbar__dropdown-link[href='/primera-division/marktwerte/wettbewerb/ES1']")))
elemento.click()

print("-------------------------------------------------------")
#print(elementos[2].get_attribute("outerHTML"))



print("pasamos el click")

input("pulse para terminar")