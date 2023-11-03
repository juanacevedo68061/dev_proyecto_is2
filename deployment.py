import os
import sys
import subprocess
import threading

def get_current_branch():
    try:
        result = os.popen('git symbolic-ref --short HEAD').read().strip()
        return result
    except Exception as e:
        print(f"Error al obtener la rama actual: {str(e)}")
        sys.exit(1)

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
            print("Error: Los cambios generan errores en el proyecto. El proyecto no se sirve adecuadamente. Proceso de deployment.py finalizado.")
            sys.exit(1)
        else:
            return True

    except Exception as e:
        print(f"Error al probar el proyecto: {str(e)}")
        sys.exit(1)

def commit_changes(commit_message):
    os.system("git add .")
    os.system(f'git commit -m "{commit_message}"')

def merge_development(branch_name):
    try:
        os.system("git config --global merge.ours.driver true")
        os.system(f"git merge -X theirs development")
        print(f"Merge de development a {branch_name} completado.")
    except Exception as e:
        print(f"Error al hacer el merge de development en {branch_name}: {str(e)}")
        sys.exit(1)

def change_branch(reference):
    if reference not in ['development', 'production']:
        print("Error: Solo se permiten las referencias 'development' y 'production'. Proceso de deployment.py finalizado.")
        sys.exit(1)

    if reference == 'production':
        branch_name = 'prueba'
    else:
        branch_name = 'development'
    
    hizo_commit = False
    current_branch = get_current_branch()
    if has_uncommitted_changes():
        if current_branch != 'development':
            print("Advertencia: En 'producción' hay cambios sin commitear. Continuar con el despliegue limpiará los cambios no commiteados.")
            user_input = input("¿Deseas continuar con el despliegue? (Sí/No): ")
            if user_input.lower() == "si" or user_input.lower() == "sí":
                os.system("git reset --hard")
                try:
                    os.system(f"git checkout {branch_name}")
                    print(f"Cambiado a la rama {branch_name}")
                    if branch_name != 'development':
                        merge_development(branch_name)
                    os.system("python manage.py runserver")
                except Exception as e:
                    print(f"Error al cambiar a la rama {branch_name}: {str(e)}")
                    sys.exit(1)
            else:
                print("Proceso de deployment.py finalizado.")
                sys.exit(1)            
        else:
            if test_project():
                commit_message = input("Por favor, ingresa un mensaje de commit para tus cambios: ")
                if not commit_message:
                    print("Error: El mensaje de commit no puede estar vacío. Proceso de deployment.py finalizado.")
                    sys.exit(1)
                commit_changes(commit_message)
                hizo_commit = True
                print("Cambios commiteados correctamente.")
                user_input = input("Aviso: El proyecto se sirve de manera adecuada, pero aún es propenso a errores en el lado del cliente. ¿Deseas continuar con el despliegue? (Sí/No): ")
                if user_input.lower() == "si" or user_input.lower() == "sí":
                    try:
                        os.system(f"git checkout {branch_name}")
                        print(f"Cambiado a la rama {branch_name}")
                        if branch_name != 'development':
                            merge_development(branch_name)
                        os.system("python manage.py runserver")
                    except Exception as e:
                        print(f"Error al cambiar a la rama {branch_name}: {str(e)}")
                        sys.exit(1)

    else:
        try:
            os.system(f"git checkout {branch_name}")
            print(f"Cambiado a la rama {branch_name}")
            print(hizo_commit)
            if hizo_commit and branch_name != 'development':
                merge_development(branch_name)
            os.system("python manage.py runserver")
        except Exception as e:
            print(f"Error al cambiar a la rama {branch_name}: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python deployment.py <referencia>")
        sys.exit(1)

    reference = sys.argv[1]
    
    change_branch(reference)