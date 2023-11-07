import subprocess

def run_docker_compose(file):
    command = ["docker-compose", "-f", file, "up", "-d"]
    subprocess.run(command, check=True)

def capture_logs_to_file(container_name, log_file):
    command = ["docker", "logs", "--follow", container_name]
    with open(log_file, "w") as log_output:
        process = subprocess.Popen(command, stdout=log_output, stderr=subprocess.STDOUT, text=True)
        process.wait()

def monitor_logs_and_execute_second_docker_compose(container_name):
    first_message = "PostgreSQL init process complete; ready for start up."
    second_message = "database system is ready to accept connections"
    log_file = "container_logs.txt"
    
    run_docker_compose("db.yml")
    capture_logs_to_file(container_name, log_file)

    with open(log_file, "r") as log_output:
        for line in log_output:
            print("contenedores =", line, end="")

            if first_message in line:
                print("\n\nDETECTOOO")

            if second_message in line:
                print("\n\nSE EJECUTÓ EL SEGUNDO DOCKER-COMPOSE")

if __name__ == "__main__":
    container_name = "proyecto_is2-db-1"
    monitor_logs_and_execute_second_docker_compose(container_name)
