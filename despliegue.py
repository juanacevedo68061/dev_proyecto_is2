import os
import subprocess
import sys

def cambiar_rama_y_desplegar(rama_objetivo):
    # Verificar la rama actual
    resultado = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
    rama_actual = resultado.stdout.strip()

    # Cambiar de rama si es necesario
    if rama_actual != rama_objetivo:
        print(f'Cambiando a la rama {rama_objetivo}')
        subprocess.run(['git', 'checkout', rama_objetivo])
    
    # Hacer un hard reset en la rama actual
    print('Haciendo git reset --hard')
    subprocess.run(['git', 'reset', '--hard'])

    # Ejecutar el servidor Django
    print('Ejecutando python manage.py runserver')
    subprocess.run(['python', 'manage.py', 'runserver'])

if __name__ == "__main__":
    # Verificar la cantidad de argumentos
    if len(sys.argv) != 2:
        print("Uso: python despliegue.py <ambiente>")
        sys.exit(1)

    ambiente = sys.argv[1]

    # Verificar el ambiente y realizar el despliegue correspondiente
    if ambiente == 'produccion':
        cambiar_rama_y_desplegar('main')
    elif ambiente == 'desarrollo':
        cambiar_rama_y_desplegar('development')
    else:
        print("Ambiente no válido. Use 'produccion' o 'desarrollo'")
        sys.exit(1)