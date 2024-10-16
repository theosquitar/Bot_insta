import random
import string
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re

# Función para generar un correo temporal usando la API de 1secmail
def generate_temp_email():
    domain = "1secmail.com"
    username = ''.join(random.choices(string.ascii_lowercase, k=7))
    email = f"{username}@{domain}"
    return email, username, domain

# Función para generar un nombre de usuario y contraseña aleatorios
def generate_random_account():
    username = ''.join(random.choices(string.ascii_lowercase, k=7)) + str(random.randint(1000, 9999))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return username, password

# Función para configurar Selenium con soporte de proxy
def setup_browser(proxy=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")  # Modo incógnito
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    
    # Si se proporciona un proxy, configurarlo
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return browser

# Función para simular pausas aleatorias (tiempos de espera)
def human_delay(min_time=3, max_time=15):
    time.sleep(random.uniform(min_time, max_time))

# Función para registrar una nueva cuenta en Instagram
def register_instagram_account(browser, email, username, password):
    browser.get('https://www.instagram.com/accounts/emailsignup/')
    
    # Esperar a que la página de registro se cargue
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, "emailOrPhone")))

    # Llenar los campos de registro
    email_input = browser.find_element(By.NAME, "emailOrPhone")
    full_name_input = browser.find_element(By.NAME, "fullName")
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")

    human_delay(3, 10)
    email_input.send_keys(email)
    
    human_delay(5, 15)
    full_name_input.send_keys("Test User")
    
    human_delay(4, 10)
    username_input.send_keys(username)
    
    human_delay(4, 10)
    password_input.send_keys(password)

    try:
        human_delay(5, 12)
        signup_button = WebDriverWait(browser, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        signup_button.click()
    except Exception as e:
        print(f"Error al hacer clic en el botón de registro: {e}")
        return False

    # Esperar a la pantalla de fecha de nacimiento
    time.sleep(10)
    
    try:
        human_delay(5, 10)
        month_dropdown = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[@title='Mes:']")))
        month_dropdown.click()
        month_option = browser.find_element(By.XPATH, "//option[@value='10']")  # Octubre
        month_option.click()

        human_delay(5, 12)
        day_dropdown = browser.find_element(By.XPATH, "//select[@title='Día:']")
        day_dropdown.click()
        day_option = browser.find_element(By.XPATH, "//option[@value='16']")  # Día 16
        day_option.click()

        human_delay(4, 12)
        year_dropdown = browser.find_element(By.XPATH, "//select[@title='Año:']")
        year_dropdown.click()
        year_option = browser.find_element(By.XPATH, "//option[@value='1995']")  # Año 1995
        year_option.click()

        human_delay(6, 12)
        next_button = browser.find_element(By.XPATH, "//button[text()='Siguiente']")
        next_button.click()

        print("Fecha de nacimiento ingresada correctamente.")
        time.sleep(7)

    except Exception as e:
        print(f"Error en la pantalla de fecha de nacimiento: {e}")
        return False

    return True

# Función para obtener el código de verificación del correo temporal
def get_verification_code(username, domain):
    inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
    for _ in range(10):  # Reintentar varias veces hasta obtener el correo
        time.sleep(20)  # Aumentar el tiempo de espera antes de verificar
        response = requests.get(inbox_url)
        messages = response.json()
        if messages:
            mail_id = messages[0]['id']
            message_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={mail_id}"
            message_response = requests.get(message_url).json()
            
            # Intentar extraer el código de verificación (usualmente son 6 dígitos)
            verification_code = re.search(r'\b\d{6}\b', message_response['body'])
            if verification_code:
                return verification_code.group(0)
    return None

# Función para ingresar el código de verificación en Instagram
def enter_verification_code(browser, code):
    try:
        # Intentar reintentar hasta encontrar el campo
        for attempt in range(5):
            try:
                # Esperar a que el campo de código de verificación esté presente
                confirmation_input = WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.NAME, "confirmationCode"))
                )
                human_delay(5, 10)
                confirmation_input.clear()
                confirmation_input.send_keys(code)
                
                # Esperar a que el botón de confirmar esté disponible y hacer clic
                submit_button = WebDriverWait(browser, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Siguiente' or text()='Confirmar']"))
                )
                human_delay(7, 12)
                submit_button.click()

                print("Código de verificación ingresado correctamente.")
                time.sleep(5)  # Esperar unos segundos para asegurar que el proceso continúa
                break  # Salir del loop si todo va bien
            except Exception as e:
                print(f"Reintentando ingresar el código, intento {attempt+1}: {e}")
                human_delay(5, 10)
        else:
            print(f"No se pudo ingresar el código tras varios intentos.")
    except Exception as e:
        print(f"Error al ingresar el código de verificación: {e}")

# Ejecutar el script
if __name__ == "__main__":
    email, username, domain = generate_temp_email()
    account_username, password = generate_random_account()

    # Usa un proxy de la lista que compartiste
    proxy = "20.111.54.16:8123"  # Proxy de Francia
    
    print(f"Generando cuenta:\nEmail: {email}\nUsername: {account_username}\nPassword: {password}")
    
    browser = setup_browser(proxy=None)  # Desactivar proxy para pruebas

    
    try:
        if register_instagram_account(browser, email, account_username, password):
            # Obtener el código de verificación del correo temporal
            verification_code = get_verification_code(username, domain)
            if verification_code:
                print(f"Código de verificación obtenido: {verification_code}")
                enter_verification_code(browser, verification_code)
                print(f"Registro exitoso. Credenciales:\nUsuario: {account_username}\nContraseña: {password}")
            else:
                print("No se pudo obtener el código de verificación.")
        else:
            print("Error en el registro.")
    finally:
        browser.quit()
