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
        test_thread.join(timeout=10)

        if test_thread.is_alive():
            test_thread.join()
            return False
        else:
            return True

    except Exception as e:
        print(f"Error al probar el proyecto: {str(e)}")
        return False

def commit_changes(commit_message):
    os.system("git add .")
    os.system(f'git commit -m "{commit_message}"')

def change_branch(branch_name, current_branch_name):
    if has_uncommitted_changes():
        if test_project():
            commit_message = input("Por favor, ingresa un mensaje de commit para tus cambios: ")
            commit_changes(commit_message)
            print("Cambios commiteados correctamente.")
            
            print("Aviso: El proyecto se sirve de manera adecuada, pero aún es propenso a errores en el lado del cliente.")
            user_input = input("¿Deseas continuar con el despliegue? (Sí/No): ")
            if user_input.lower() == "si" or user_input.lower() == "sí":
                try:
                    os.system(f"git checkout {branch_name}")
                    print(f"Cambiado a la rama {branch_name}")
                    
                    # Realiza un merge de la rama actual en la rama de destino con mensaje personalizado
                    merge_message = f"Merge de {branch_name}"
                    os.system(f"git merge {current_branch_name} -m '{merge_message}'")
                    
                    print(f"Merge de {current_branch_name} a {branch_name} completado.")
                except Exception as e:
                    print(f"Error al cambiar a la rama {branch_name}: {str(e)}")
                    sys.exit(1)
            else:
                print("No se ha cambiado de rama. Proceso de deployment.py finalizado.")
        else:
            print("Error: Los cambios generan errores en el proyecto. El proyecto no se sirve adecuadamente. Proceso de deployment.py finalizado.")
    else:
        try:
            os.system(f"git checkout {branch_name}")
            print(f"Cambiado a la rama {branch_name}")
        except Exception as e:
            print(f"Error al cambiar a la rama {branch_name}: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python deployment.py <branch_name>")
        sys.exit(1)

    branch_name = sys.argv[1]
    
    # Obtiene el nombre de la rama actual
    current_branch_name = os.popen('git branch --show-current').read().strip()
    
    change_branch(branch_name, current_branch_name)
