import subprocess
import sys

def run_docker_compose(file):
    command = ["docker-compose", "-f", file, "up", "-d"]
    subprocess.run(command, check=True)

def run_second_docker_compose():
    with open("second_docker_compose.log", "w") as log_file:
        command = ["docker-compose", "-f", "docker-compose.yml", "up", "-d"]
        process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            sys.stdout.write(line)

        process.wait()

def monitor_logs_and_execute_second_docker_compose(container_name):
    first_message = "PostgreSQL init process complete; ready for start up."
    process = subprocess.Popen(["docker", "logs", "--follow", container_name], stdout=subprocess.PIPE, text=True)

    for line in process.stdout:
        print("contenedores = ", line, end="")

        if first_message in line:
            print("\n\nEMPIEZA EL SEGUNDO DOCKER-COMPOSE")
            run_second_docker_compose()

if __name__ == "__main__":
    container_name = "proyecto_is2-db-1"

    run_docker_compose("db.yml")

    monitor_logs_and_execute_second_docker_compose(container_name)
