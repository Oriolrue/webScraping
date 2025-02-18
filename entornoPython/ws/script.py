from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pymysql

# Configuración de Selenium
options = Options()
options.headless = False  # Cambia a True si deseas ejecución en segundo plano
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
        # 🔴 Eliminar primero los registros de las tablas dependientes
        cursor.execute("DELETE FROM lore")
        cursor.execute("DELETE FROM image")
        cursor.execute("DELETE FROM murmur")  # Finalmente, eliminar de la tabla principal

        # Confirmar cambios
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

    # Obtener los nombres de los enemigos
    enemies = driver.find_elements(By.CLASS_NAME, 'wds-tabs__tab')
    descriptions = driver.find_elements(By.CLASS_NAME, 'codexflower')


    # Insertar los nuevos datos
    with connection.cursor() as cursor:
        for i in range(len(enemies)):
            name = enemies[i].find_element(By.TAG_NAME, 'a').text

            # Insertar en murmur
            sql_murmur = "INSERT INTO murmur (name) VALUES (%s)"
            cursor.execute(sql_murmur, (name,))
            murmur_id = cursor.lastrowid  # Obtener el ID recién insertado

            # Insertar en lore (si hay descripción correspondiente)
            if i < len(descriptions):
                desc = descriptions[i].text.strip()
                sql_lore = "INSERT INTO lore (id, description) VALUES (%s, %s)"
                cursor.execute(sql_lore, (murmur_id, desc))

        connection.commit()

    print("✅ Datos insertados correctamente.")

finally:
    # Cerrar la conexión y el navegador
    connection.close()
    driver.quit()