import subprocess

def run_docker_compose(file):
    command = ["docker-compose", "-f", file, "up", "-d"]
    subprocess.run(command, check=True)

def monitor_logs_and_execute_second_docker_compose(container_name):
    first_message = "PostgreSQL init process complete; ready for start up."
    process = subprocess.Popen(["docker", "logs", "--follow", container_name], stdout=subprocess.PIPE, text=True)

    second_docker_logs = open("second_docker_compose.log", "w")

    for line in process.stdout:
        print("contenedores = ", line, end="")
        second_docker_logs.write(line)  # Guarda los logs en un archivo

        if first_message in line:
            print("\n\nEMPIEZA EL SEGUNDO DOCKER-COMPOSE")
            run_docker_compose("docker-compose.yml")
            print("\n\nSE EJECUTÓ EL SEGUNDO DOCKER-COMPOSE")

    second_docker_logs.close()

if __name__ == "__main__":
    container_name = "proyecto_is2-db-1"

    run_docker_compose("db.yml")

    monitor_logs_and_execute_second_docker_compose(container_name)
