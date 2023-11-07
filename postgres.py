import subprocess
import os
from time import sleep 

def run_docker_compose(file):
    command = f"docker-compose -f {file} up -d"
    os.system(command)

def monitor_logs_and_execute_second_docker_compose(container_name):
    mensaje = "PostgreSQL init process complete; ready for start up."
    process = subprocess.Popen(["docker", "logs", "--follow", container_name], stdout=subprocess.PIPE, text=True)
    bandera = False
    for linea in process.stdout:
        print("POSTGRES =", linea, end="")

        if mensaje in linea:
            print("\nEsperando 5 segundos...")
            sleep(5)
            bandera = True

        if bandera:
            print("\nSE COMPLETO!")
            break

if __name__ == "__main__":
    container_name = "proyecto_is2-db-1"
    run_docker_compose("db.yml")
    monitor_logs_and_execute_second_docker_compose(container_name)
