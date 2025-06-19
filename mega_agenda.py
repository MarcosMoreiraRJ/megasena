import schedule # Importa 'schedule' que permite agendar tarefas para serem executadas em horários específicos
import time # Importa 'time' para usar funções relacionadas ao tempo, como sleep (pausa)
import subprocess # Importa 'subprocess' para executar comandos e scripts externos (como outro arquivo Python)

# Define uma função que executa o script 'mega_atualiza.py'
def executar_script():
    subprocess.run(["python", "mega_atualiza.py"])  # Executa o script usando o interpretador Python

# Agenda a execução da função 'executar_script' para às quartas-feiras às 21:00 (horário local do sistema)
schedule.every().wednesday.at("21:00").do(executar_script)

# Agenda a execução da função 'executar_script' para aos sábados às 21:00
schedule.every().saturday.at("21:00").do(executar_script)

# Imprime uma mensagem informando que o agendamento foi iniciado
print("Agendamento iniciado. Aguardando horários...")

# Cria um loop infinito que verifica constantemente se alguma tarefa agendada deve ser executada
while True:
    schedule.run_pending()  # Executa qualquer tarefa que esteja agendada para o horário atual
    time.sleep(60)          # Aguarda 60 segundos antes de verificar novamente (reduz uso de CPU)