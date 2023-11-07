import subprocess
import os

def run_docker_compose(file):
    command = f"docker-compose -f {file} up -d"
    os.system(command)

def monitor_logs_and_execute_second_docker_compose(container_name):
    first_message = "CREATE DATABASE"
    second_message = "database system is ready to accept connections"

    state = 0

    process = subprocess.Popen(["docker", "logs", "--follow", container_name], stdout=subprocess.PIPE, text=True)

    for line in process.stdout:
        print("contenedores = ", line, end="")

        if state == 0 and first_message in line:
            state = 1
        elif state == 1 and second_message in line:
            print("\n\nEMPIEZA EL SEGUNDO DOCKER-COMPOSE")
            run_docker_compose("docker-compose.yml")
            print("\n\nSE EJECUTÓ EL SEGUNDO DOCKER-COMPOSE")
if __name__ == "__main__":
    container_name = "proyecto_is2-db-1"

    run_docker_compose("db.yml")

    monitor_logs_and_execute_second_docker_compose(container_name)  # Monitorea los logs y ejecuta el segundo archivo
