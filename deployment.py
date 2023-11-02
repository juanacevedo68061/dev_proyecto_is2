import os
import sys
import subprocess
import threading

def has_uncommitted_changes():
    try:
        result = os.system("git diff-index --quiet HEAD --")
        return result != 0
    except Exception as e:
        print(f"Error al verificar cambios sin commitear: {str(e)}")
        sys.exit(1)

def test_project():
    try:
        def test_server():
            subprocess.run(["python", "manage.py", "runserver"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        test_thread = threading.Thread(target=test_server)
        test_thread.start()
        test_thread.join(timeout=10)  # Espera hasta 10 segundos, ajusta el tiempo según tus necesidades

        if test_thread.is_alive():
            test_thread.join()  # Si el servidor aún se está ejecutando después del tiempo de espera, lo detenemos
            return False
        else:
            return True

    except Exception as e:
        print(f"Error al probar el proyecto: {str(e)}")
        return False

def commit_changes(commit_message):
    os.system("git add .")
    os.system(f'git commit -m "{commit_message}"')

def change_branch(branch_name):
    if has_uncommitted_changes():
        if test_project():
            commit_message = input("Por favor, ingresa un mensaje de commit para tus cambios: ")
            commit_changes(commit_message)
            print("Cambios commiteados correctamente.")

    if test_project():
        print("El proyecto se sirve de forma adecuada.")
        if has_uncommitted_changes():
            print("¿Deseas cambiar de rama? (Sí/No): ")
            user_input = input()
            if user_input.lower() == "si" or user_input.lower() == "sí":
                try:
                    os.system(f"git checkout {branch_name}")
                    print(f"Cambiado a la rama {branch_name}")
                except Exception as e:
                    print(f"Error al cambiar a la rama {branch_name}: {str(e)}")
                    sys.exit(1)
            else:
                print("Cambios commiteados pero no se ha cambiado de rama.")
        else:
            try:
                os.system(f"git checkout {branch_name}")
                print(f"Cambiado a la rama {branch_name}")
            except Exception as e:
                print(f"Error al cambiar a la rama {branch_name}: {str(e)}")
                sys.exit(1)
    else:
        print("El proyecto no se sirve de forma adecuada. Por favor, corrige los errores antes de cambiar de rama.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python deployment.py <branch_name>")
        sys.exit(1)

    branch_name = sys.argv[1]
    change_branch(branch_name)
