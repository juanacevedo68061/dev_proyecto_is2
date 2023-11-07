import subprocess

def run_docker_compose(file):
    command = ["docker-compose", "-f", file, "up", "-d"]
    subprocess.run(command, check=True)

def monitor_logs_and_execute_second_docker_compose(container_name):
    first_message = "PostgreSQL init process complete; ready for start up."
    second_message = "database system is ready to accept connections"
    received_first_message = False
    log_file = "container_logs.txt"

    process = subprocess.Popen(["docker", "logs", "--follow", "--tail", "all", container_name], stdout=subprocess.PIPE, text=True)

    with open(log_file, "w") as log_output:
        for line in process.stdout:
            log_output.write(line)
            log_output.flush()
            print("contenedores = ", line, end="")

            if first_message in line:
                received_first_message = True
                print("\n\nDETECTOOO")

            if received_first_message and second_message in line:
                print("\n\nSE EJECUTÓ EL SEGUNDO DOCKER-COMPOSE")

if __name__ == "__main__":
    container_name = "proyecto_is2-db-1"

    run_docker_compose("db.yml")
    monitor_logs_and_execute_second_docker_compose(container_name)
