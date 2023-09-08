import sys
sys.path.append('/app')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')
import django
django.setup()

import pandas as pd
import inspect
from django.test import TestCase
from datetime import datetime

def recopilar_datos_tests(ruta_script):
    try:
        data = []

        modulo_name = ruta_script.replace('/app/', '').replace('/', '.').replace('.py', '')
        modulo = __import__(modulo_name, fromlist=[''])
        fecha_actual = datetime.now().strftime('%d-%m-%Y')

        for nombre, objeto in inspect.getmembers(modulo):
            if inspect.isclass(objeto) and issubclass(objeto, TestCase) and objeto is not TestCase:
                for metodo_nombre, metodo_objeto in inspect.getmembers(objeto):
                    if metodo_nombre.startswith('test_'):
                        data.append({
                            "SCRIPT": ruta_script.split('/')[-1],
                            "METODO": metodo_nombre,
                            "FECHAPRU": fecha_actual,
                            "MODULO": modulo_name.split('.')[0]
                        })

        return data
    except Exception as e:
        print(f"Error al procesar {ruta_script}: {e}")
        return []

# Lista de módulos
modulos = ['login', 'administracion', 'roles', 'canvan', 'publicaciones']

archivos_tests = []

for modulo in modulos:
    directorio_tests = os.path.join("/app", modulo, "tests")
    if os.path.exists(directorio_tests):
        for f in os.listdir(directorio_tests):
            if f.startswith('test_') and f.endswith('.py'):
                archivos_tests.append(os.path.join(directorio_tests, f))

print(f"Archivos de prueba encontrados: {archivos_tests}")

# Dataframe inicial
df = pd.DataFrame(columns=["SCRIPT", "METODO", "FECHAPRU", "MODULO"])

# Llenar el dataframe
dfs = []
for archivo in archivos_tests:
    data = recopilar_datos_tests(archivo)
    dfs.append(pd.DataFrame(data))

df = pd.concat(dfs, ignore_index=True)

print(f"Datos recopilados: \n{df}")

# Definir el nombre del archivo
filename = "EQUIPO_06_CONTROL_PRUEBAS_UNITARIAS.xlsx"
df = df.reset_index(drop=True)
df["ITEM"] = range(1, len(df) + 1)# Añade la columna ITEM con un valor incremental
# df = df.reset_index(drop=True)
df["REVISADO EN SPRINT"] = ""  # agregar valor que se desee
df["RESPONSABLE"] = ""  # agregar nombre que se desee

# Las columnas 
column_order = ["ITEM", "MODULO", "SCRIPT", "METODO", "FECHAPRU", "REVISADO EN SPRINT", "RESPONSABLE"]
df = df[column_order]

with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    workbook = writer.book
    worksheet = workbook.create_sheet("Pruebas Unitarias", 0)  # Crear y hacer esta hoja la primera
    workbook.active = worksheet  # Activar la hoja

    # Añadir encabezados y títulos
    worksheet.merge_cells('A1:G1')
    worksheet.cell(row=1, column=1).value = "EQUIPO NRO: 06" 

    worksheet.merge_cells('A3:G3')
    worksheet.cell(row=3, column=1).value = "PLANILLA DE CONTROL DE PRUEBAS UNITARIAS"

    
    df.to_excel(writer, sheet_name="Pruebas Unitarias", startrow=7, index=False, header=False)  # El DataFrame comienza en la fila 7, y sin el encabezado ya que vamos a agregarlo manualmente
    
    # Añadir el encabezado manualmente
    headers = ["ITEM", "MODULO", "SCRIPT", "METODO", "FECHA PRU", "REVISADO EN SPRINT", "RESPONSABLE"]
    for col_num, value in enumerate(headers, 1):
        cell = worksheet.cell(row=7, column=col_num, value=value)  # Añadir el encabezado en la fila 7
        cell.font = cell.font.copy(bold=True)
print(f'Archivo "{filename}" generado con éxito!')
