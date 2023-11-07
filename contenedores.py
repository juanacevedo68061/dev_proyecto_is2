import subprocess
import os

def run_docker_compose(file):
    command = f"docker-compose -f {file} up -d"
    os.system(command)

def monitor_logs_and_execute_second_docker_compose(container_name):
    mensaje = "PostgreSQL init process complete; ready for start up."
    process = subprocess.Popen(["docker", "logs", "--follow", container_name], stdout=subprocess.PIPE, text=True)

    for linea in process.stdout:
        print("POSTGRES =", linea, end="")

        if mensaje in linea:
            print("\nSE EJECUTA DOCKER-COMPOSE")

if __name__ == "__main__":
    container_name = "nombre_del_contenedor"
    run_docker_compose("db.yml")
    monitor_logs_and_execute_second_docker_compose(container_name)
