from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymysql

# Configuración de Selenium
options = Options()
options.headless = False  # Cambia a True para ejecución en segundo plano
driver = webdriver.Chrome(options=options)

# Conexión a la base de datos
connection = pymysql.connect(
    host="localhost",
    user="usuario",
    password="password",
    database="enemieframe"
)

try:
    with connection.cursor() as cursor:
        # 🔴 Eliminar registros previos
        cursor.execute("DELETE FROM lore")
        cursor.execute("DELETE FROM image")
        cursor.execute("DELETE FROM murmur")
        connection.commit()
        print("🔄 Datos antiguos eliminados correctamente.")

    # Abrir la página web
    driver.get("https://warframe.fandom.com/wiki/The_Murmur")
    time.sleep(3)

    # Aceptar cookies (si es necesario)
    try:
        cookies_button = driver.find_element(By.CLASS_NAME, '_2O--J403t2VqCuF8XJAZLK')
        cookies_button.click()
        time.sleep(3)
    except:
        print("⚠️ No se encontró el botón de cookies.")

    # Obtener todas las pestañas de los enemigos
    enemy_tabs = driver.find_elements(By.CLASS_NAME, 'wds-tabs__tab')

    for index, tab in enumerate(enemy_tabs):
        name = tab.text.strip()

        # 🔹 Hacer clic en la pestaña con JavaScript
        driver.execute_script("arguments[0].click();", tab)
        time.sleep(3)  # Esperar un poco más para asegurarnos de que la página haya cargado

        # 🔹 Intentar esperar a que la descripción se cargue (con un tiempo de espera más largo)
        try:
            # Esperamos que el contenedor de la descripción esté presente
            description_container = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'codexflower'))
            )

            # 🔹 Hacer scroll dentro del div con overflow: auto
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", description_container)
            time.sleep(2)  # Esperar un momento después de hacer scroll para que el contenido se cargue

            # 🔹 Verificar que el contenido sea visible después de hacer scroll
            visible_text = description_container.get_attribute("textContent").strip()

            # Si no se obtiene texto, realizar otro scroll
            if not visible_text:
                print(f"⚠️ Descripción vacía para {name}. Haciendo más scroll...")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", description_container)
                time.sleep(3)  # Esperar un poco más

                visible_text = description_container.get_attribute("textContent").strip()

            # Si aún no hay texto, marcar como no encontrado
            if not visible_text:
                visible_text = "Descripción no encontrada"

        except Exception as e:
            visible_text = "Descripción no encontrada"
            print(f"⚠️ Error al obtener la descripción para {name}: {e}")

        # Insertar en la base de datos
        with connection.cursor() as cursor:
            sql = "INSERT INTO murmur (name) VALUES (%s)"
            cursor.execute(sql, (name,))
            murmur_id = cursor.lastrowid

            sql = "INSERT INTO lore (id, description) VALUES (%s, %s)"
            cursor.execute(sql, (murmur_id, visible_text))

        connection.commit()
        print(f"✅ Guardado: {name} - {visible_text}")

    print("✅ Todos los datos han sido insertados correctamente.")

finally:
    connection.close()
    driver.quit()
