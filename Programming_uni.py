from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


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
import pandas as pd



def generar_fechas():
    fechas = []
    fecha_actual = datetime(2010, 11, 1)  # Fecha de inicio
    fecha_final = datetime(2024, 3, 1)  # Fecha final

    while fecha_actual <= fecha_final:
        fechas.append('"' + fecha_actual.strftime("%d/%m/%Y") + '"')
        if fecha_actual.day == 1:
            fecha_actual += timedelta(days=14)  # Aumentar 14 días si es el primer día del mes
        else:
            fecha_actual = datetime(fecha_actual.year if fecha_actual.month < 12 else fecha_actual.year + 1,
                                    fecha_actual.month % 12 + 1,
                                    1)  # Ir al primer día del siguiente mes
    
    return fechas

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
wait = WebDriverWait(driver,30) # tiempo de espera hasta que el elemento este disponible

#print("antes de entrar en la pagina")

driver.get("https://www.transfermarkt.es/")

iframe = driver.find_element(By.CSS_SELECTOR, "iframe#sp_message_iframe_1015264")

driver.switch_to.frame(iframe)


cookies = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,"button.message-component.message-button.no-children.focusable.accept-all.sp_choice_type_11.first-focusable-el"))) 

cookies.click()

driver.switch_to.default_content()

barra = driver.find_element(By.CSS_SELECTOR,"ul.main-navbar__container")
valoresBarra = barra.find_elements(By.CSS_SELECTOR,"li")

elemento = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//span[starts-with(@id, 'ASTAGQ_plc_close_')]")))     ### Para quitar la publi
elemento.click()


def valoresEquipos():
    valoresDeMercadoSpan = valoresBarra[2].find_element(By.CSS_SELECTOR,"span").click()         ### Click de Valores de Mercado

    elemento = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a.main-navbar__dropdown-link[href='/primera-division/marktwerte/wettbewerb/ES1']")))
    elemento.click()


    shadow_host = driver.find_element(By.CSS_SELECTOR, 'tm-subnavigation[controller="wettbewerb"][id="ES1"][season="2023"][section="wettbewerb"][style="display: block; margin: 0 5px;"')
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    element_inside_shadow_dom = shadow_root.find_element(By.CSS_SELECTOR, 'div').find_element(By.CSS_SELECTOR,"ul")

    todosLi = element_inside_shadow_dom.find_elements(By.CSS_SELECTOR,"li.svelte-e7ru94.arrow")

    #MIRAR SI SE PUEDE BORRAR
    x=0  
    while x <2:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        x = x +1

    liSolo = todosLi[2]
    clicValoresMercado = liSolo.find_element(By.CSS_SELECTOR,"a")


    clicValoresMercado.click()

    vistaGeneral = liSolo.find_element(By.CSS_SELECTOR,"dd").find_elements(By.CSS_SELECTOR,"li")
    elementoValoresClubes = vistaGeneral[1].find_element(By.CSS_SELECTOR,"a")
    elementoValoresClubes.click()

    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #Estos son todas las casillas donde estan los nombres,fecha y valor de cada club 
    #elementos = driver.find_element(By.CSS_SELECTOR,"table.items").find_element(By.CSS_SELECTOR,"tbody").find_elements(By.CSS_SELECTOR,"tr")
    
    #print("-------------------------------------------------------")

    fijador = driver.find_element(By.CSS_SELECTOR, "h1.content-box-headline")
    driver.execute_script("arguments[0].scrollIntoView();",fijador)

    fechas_generadas = generar_fechas()

    time.sleep(1)

    #print("\n\n")  
    #print("-----------------------------------")


    #Estos son todas las casillas donde estan los nombres,fecha y valor de cada club 
    elementos = driver.find_element(By.CSS_SELECTOR,"table.items").find_element(By.CSS_SELECTOR,"tbody").find_elements(By.CSS_SELECTOR,"tr")
    #print(elementos[0].get_attribute("outerHTML")) 
    #print("\n\n")  
    #print("-----------------------------------")

    fijador = driver.find_element(By.CSS_SELECTOR, "h1.content-box-headline")
    driver.execute_script("arguments[0].scrollIntoView();",fijador)


    time.sleep(1)

    df = pd.DataFrame(columns=['Nombre Equipo', 'Valor Equipo (en millones $)', 'Fecha'])

    #'''
    contadorDF = 0
    iter = 0
    i=0
    while i < len(fechas_generadas):
        #print(f"ENTRANDO EN LA ITERACION NUMERO {i}")

        #fijador = driver.find_element(By.CSS_SELECTOR, "h1.content-box-headline")
        #driver.execute_script("arguments[0].scrollIntoView();",fijador)

        try:
            time.sleep(1)
            #barraFecha = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "div.inline-select div")))  # Combine selectors directly
            barraFecha = driver.find_element(By.CSS_SELECTOR,"div.inline-select").find_element(By.CSS_SELECTOR,"div")
            #print(barraFecha.get_attribute("outerHTML"))      
            barraFecha.click()
            #time.sleep(20)
            #barraEscribir = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search'][autocomplete='off'][tabindex='0']")))
            barraEscribir = driver.find_element(By.CSS_SELECTOR,"input[type='search'][autocomplete='off'][tabindex='0']")
        
            #print(f"esta es la fecha que tiene que escribir {fechas_generadas[i]}")
        
            barraEscribir.send_keys(fechas_generadas[i].replace('"', ''))
            barraEscribir.send_keys(Keys.ENTER)
        
        except:
            #print("me fui por la execption")
            time.sleep(1)
            continue

        #time.sleep(1)
        botonMostar = driver.find_element(By.CSS_SELECTOR,"input[type='submit'].right.small.button")
        botonMostar.click()
        x = 0
        #wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "td.hauptlink a")))
        #print(elementos[x].find_element(By.CSS_SELECTOR,"td.hauptlink a").text)
        elementos = driver.find_element(By.CSS_SELECTOR,"table.items").find_element(By.CSS_SELECTOR,"tbody").find_elements(By.CSS_SELECTOR,"tr")
        
        
        while x<=2:
            wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "tr td.hauptlink a")))
            
            nombre = elementos[x].find_element(By.CSS_SELECTOR,"tr td.hauptlink a").text
            valor = elementos[x].find_element(By.CSS_SELECTOR,"tr td.rechts a").text

            #print(f"este equipo:{nombre} tiene este valor {valor}")
            
            if "mil mill. €" in valor:
                mult = 1000000000
                
            else:
                mult = 1000000
                

            valor_sin_formato = valor.split(" ")[0].replace(",", "")  # Extract before space, remove comma
            valor_entero = int(valor_sin_formato) * mult

            

            df.loc[contadorDF] = [nombre,
                        valor_entero,
                        fechas_generadas[i].replace('"','')]     
            contadorDF = contadorDF + 1
            
            x = x +1
        #print(f"SALIENDO DE LA ITERACION NUMERO {i}")
        i = i + 24
        #24 es un año
        df.to_csv("valoresEquipo.csv", index=False, sep=',')

        #print(elemento.get_attribute("outerHTML"))   
        #print(nombreEquipo.get_attribute("outerHTML"))  
    #'''
    #print("---------------------------")
    #print("\n\n")

    print(df)

#time.sleep(1)
valoresDeMercadoSpan = valoresBarra[2].find_element(By.CSS_SELECTOR,"span").click()         ### Click de Valores de Mercado

elemento = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a.main-navbar__dropdown-link[href='/primera-division/marktwerte/wettbewerb/ES1']")))
elemento.click()

'''
shadow_host = driver.find_element(By.CSS_SELECTOR, 'tm-subnavigation[controller="wettbewerb"][id="ES1"][season="2023"][section="wettbewerb"][style="display: block; margin: 0 5px;"')
shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
element_inside_shadow_dom = shadow_root.find_element(By.CSS_SELECTOR, 'div').find_element(By.CSS_SELECTOR,"ul")
'''


fijador = driver.find_element(By.CSS_SELECTOR, "h1.content-box-headline")
driver.execute_script("arguments[0].scrollIntoView();",fijador)

tablaJugadores = driver.find_element(By.CSS_SELECTOR,"div.responsive-table").find_element(By.CSS_SELECTOR,"tbody").find_elements(By.CSS_SELECTOR,"tr")

class JugadorFutbol:
    def __init__(self, nombreCompleto: str, valorMercado: int, club: str):
        self.nombreCompleto = nombreCompleto
        self.valorMercado = valorMercado
        self.club = club

    def __str__(self):
        return f"Nombre: {self.nombreCompleto}\nValor de mercado: {self.valorMercado}\nClub: {self.club}"

jugadoresMadrid = 0
jugadoresBarca = 0
jugadoresReal = 0
suma = 0  
x = 0

futbolistas = []
while suma != 9 and x != 10:


    soccerPlayer = tablaJugadores[x].find_elements(By.CSS_SELECTOR,"td")

    print(soccerPlayer[1].get_attribute("outerHTML"))  

    equipo = soccerPlayer[7].find_element(By.CSS_SELECTOR,"a").get_attribute("title") 

    if equipo == "Real Madrid CF" and jugadoresMadrid == 3:
        pass

    elif equipo == "FC Barcelona" and jugadoresBarca == 3:
        pass

    elif equipo == "Real Sociedad" and jugadoresReal == 3:
        pass
    else:

        nombre = soccerPlayer[1].find_element(By.CSS_SELECTOR,"tr").find_elements(By.CSS_SELECTOR,"td")[1].find_element(By.CSS_SELECTOR,"a").text
        
        valorJugador = soccerPlayer[8].find_element(By.CSS_SELECTOR,"a").text

        valor_sin_formato = valorJugador.split(" ")[0].replace(",", "")  # Extract before space, remove comma
        valor_entero = int(valor_sin_formato) * 1000000

        futbolista = JugadorFutbol(nombre,valor_entero,equipo)
        futbolistas.append(futbolista)

        if equipo == "Real Madrid CF" and jugadoresMadrid == 3:
            jugadoresMadrid = jugadoresMadrid +1

        elif equipo == "FC Barcelona" and jugadoresBarca == 3:
            jugadoresBarca = jugadoresBarca + 1

        elif equipo == "Real Sociedad" :
            jugadoresReal = jugadoresReal + 1

        suma = jugadoresMadrid + jugadoresBarca + jugadoresReal

        x = x +1 
#print(equipo.get_attribute("outerHTML"))  
        
print(futbolistas)

print("\n\n")

input("pulse para terminar")    