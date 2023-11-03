import os

# Ejecutar los scripts de carga en orden
os.system("python poblacion/carga_usuarios.py")
os.system("python poblacion/carga_categorias.py")
os.system("python poblacion/carga_publicaciones.py")
