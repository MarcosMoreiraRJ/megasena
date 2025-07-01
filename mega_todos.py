import csv
import time
import re
import os
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

csv_filename = "resultados_megasena.csv"

def obter_ultimo_concurso_salvo():
    if not os.path.exists(csv_filename):
        return 0
    with open(csv_filename, "r", encoding="utf-8") as f:
        linhas = list(csv.reader(f))
        if len(linhas) < 2:
            return 0
        ultimo = linhas[-1][0]
        return int(ultimo)

# Se o arquivo não existir, cria com cabeçalho
if not os.path.exists(csv_filename):
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Concurso", "Data", "Dezenas"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")

    # Pega o número do concurso mais recente publicado
    span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.ng-binding")))
    match = re.search(r"Concurso\s+(\d+)", span.text)
    concurso_mais_recente = int(match.group(1)) if match else 0

    ultimo_concurso_salvo = obter_ultimo_concurso_salvo()
    print(f"Último na planilha: {ultimo_concurso_salvo}")
    print(f"Mais recente no site: {concurso_mais_recente}")

    novos_concursos = False

    for i in range(ultimo_concurso_salvo + 1, concurso_mais_recente + 10):  # tenta buscar até 10 a mais, se houver
        try:
            input_busca = wait.until(EC.presence_of_element_located((By.ID, "buscaConcurso")))
            input_busca.clear()
            input_busca.send_keys(str(i))
            input_busca.send_keys(Keys.ENTER)

            # Espera o número aparecer ou desiste se não carregar
            time.sleep(2)  # pequena espera para a mudança de conteúdo

            try:
                # Verifica se o concurso existe na página (texto do concurso deve bater)
                span_atual = driver.find_element(By.CSS_SELECTOR, "span.ng-binding")
                if f"Concurso {i}" not in span_atual.text:
                    print(f"Concurso {i} ainda não está disponível.")
                    break  # esse número (e os próximos) ainda não existem
            except NoSuchElementException:
                print(f"Concurso {i} ainda não disponível (nenhum span encontrado).")
                break

            ul = wait.until(EC.presence_of_element_located((By.ID, "ulDezenas")))
            numeros = [li.text for li in ul.find_elements(By.TAG_NAME, "li")]

            m = re.search(r"Concurso\s+(\d+)\s+\(([\d/]+)\)", span_atual.text)
            concurso_num = m.group(1)
            concurso_data = m.group(2)

            with open(csv_filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([concurso_num, concurso_data, ", ".join(numeros)])

            print(f"Concurso {concurso_num} [{concurso_data}]: {numeros}")
            novos_concursos = True

        except (TimeoutException, NoSuchElementException, WebDriverException) as sub_e:
            print(f"Erro ao buscar concurso {i}: {sub_e}")
            traceback.print_exc()
            break  # não continua se erro pode ser de concurso inexistente

        time.sleep(1)

    if not novos_concursos:
        print("Planilha Atualizada.")

except Exception as e:
    print("Erro durante o processo principal:", e)
    traceback.print_exc()
finally:
    driver.quit()
    print("\nProcesso encerrado.")
