#Drivers de selenium
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# modificar las opciones de webdriver en chrome
from selenium.webdriver.chrome.options import Options
# definir el tipo de busqueda del elemento
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as ec  # para condiciones en selenium
from selenium.common.exceptions import TimeoutException # exception de timeout en selenium
from config_instagram import * #importar las credenciales para instagram
import time
import pickle # Para cargar/Guardar cookies


def cursor_arriba(n=1):
    """Subir el cursor n veces"""
    print(f'\n033{n}A', end="")

def rata():
    print("-"*os.get_terminal_size().columns)

def inicar_chrome():

    ruta =  'chromedriver\\chromedriver.exe'

    #OPCIONES DE GOOGLE CHROME
    options = Options()#instanciamos opciones de chrome 

    #options.add_argument("--headless") #iniciar iminimizado
    options.add_argument("--window-size=970,1080")
    #options.add_argument("--start-maximized") #iniciar pestaña maximizada 
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions") #no cargar extensiones de chrome 
    options.add_argument("--disable-notifications") #bloquear notificaciones de chrome 
    options.add_argument("--ignore-certificate-errors") #no mostrar el aviso de conexion no privada
    options.add_argument("--no-sandbox") #desabilita el modo sandbox
    options.add_argument("--log-level=3")  #evitar que se muestren mensajes en la terminal (solo se mostraran errores)
    options.add_argument("--no-default-browser-check") #Evitar el aviso de que chrome no es un navegador por defecto
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled") #oculto que soy un bot ya que sistemas anti bot utilizan el comando navigator.webdriver

    # PARAMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER
    exp_opt = [
        'enable-automation', #No mostrar la notificacion de un software automatizado
        'ignore-certificate-errors' #ignorar errores de certificados
        'enable-logging'#no mostrar por consola "DevTools listening on...."
            ]

    options.add_experimental_option("excludeSwitches", exp_opt)

    #PARAMETROS QUE DEFINEN LA PREFERENCIA EN CHROMEDRIVERS
    prefs = {
        "profile.default_content_setting_values.notifications": 2, #notificaciones: 0 = preguntar | 1 = permitir | 2 = no permitir
        "intl.accept_languages": ["es-ES", "es"], #para definir el idioma del navegador
        "credentials_enable_service": False #evitar que chrome nos pregunte si queremos guardar nuestra contraseña al loggiarnos
    }
    options.add_experimental_option("prefs", prefs)


    #instanciamos el servicio de chromedriver
    service = Service(executable_path=ruta)
    service.start()
    #instanciamos webdriver de selenium con chrome
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_position(0,0)
    #devolvemos el driver
    return driver


def login_instagram():
    """Realizar login en instagram, si es posbile por cookis y sino desde cero"""

    #Comprobamos si existen las cookies
    if os.path.isfile("instagram.cookies"):
        #Leemos las cookies del archivo local
        cookies = pickle.load(open("instagram.cookies", "rb"))
        #Iniciamos la paginaa de instagram robots.txt
        driver.get("https://www.instagram.com/robots.txt")
        #Recorremos el objeto cookies y las añadimos al driver
        for cookie in cookies:
            driver.add_cookie(cookie)
        #abrimos la pagina de instagram
        driver.get("https://www.instagram.com/")
        #Comprobamos  el login por cooki funciona 
        try:
            #Verificamos si existe el componente css article
            elemento = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "article")))
            print("Login por cookie realizado con exito") 
            return "OK"
        except TimeoutException:
            print("ERROR: El feed de noticias no se acargado exitosamente")
            return "ERROR"  

    #Abrimos la paginade INSTAGRAM
    print('Login en INSTAGRAM desde CERO')
    driver.get("https://www.instagram.com/")
    try:
        #Esperamos a que el elemento de username se encuentre disponible  
        elemento = wait.until(ec.visibility_of_element_located((By.NAME, "username")))
    #Si el tiempo de espera supera el tiempo definido entra a la excepcion
    except TimeoutException:
        print("Error:Elemento 'username' no disponible ")
        return "ERROR"    
    #Al cargar elemento escribimos el usuario 
    elemento.send_keys(USER_IG)    
    #Esperamos que se carga el elemento de password
    elemento = wait.until(ec.visibility_of_element_located((By.NAME, "password"))) #Localizar elemento
    #Al cargar el elemento escribimos la contraseña 
    elemento.send_keys(PASSWORD_IG)  
    #Esperamos que carga el boton submit
    elemento = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    #Presionanos el boton sybmit
    elemento.click()
    #Esperamos que carga la informacion de guardar informacion
    elemento = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[text()='Guardar información']")))
    #le damos click al boton de guardas infomracion
    elemento.click()
    try:
        elemento = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "article")))
        print("Login realizado con exito") 
    except TimeoutException:
        print("ERROR: El feed de noticias no se acargado exitosamente")
        return "ERROR"   
    
    # Guardar cookis de la pagina para que iniciar sesion sea mas rapido
    cookies = driver.get_cookies()
    pickle.dump(cookies, open("instagram.cookies", "wb"))
    print("cokies guardadas")


    print("ok")
#Quede en el minuto 24:30

# MAIN ############################################################################
if __name__ == '__main__':
    #iniciamos selenium
    driver = inicar_chrome()
    #configuramos el tiempo de espera para cargar elementos
    wait = WebDriverWait(driver, 10) #tiempo de espera hasta que el elmento esta disponible
    # nos loguiamos en instagram
    res = login_instagram()
    if res == "ERROR": #si se produce un error en login
        input("Pulsa ENTER para salir...") #pausa para studiar el error
        driver.quit()#cerramos chrome
        sys.exit(1) #salimos del programa
    input("Pulsar ENTER para salir")
    driver.quit()