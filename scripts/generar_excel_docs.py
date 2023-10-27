import os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Ruta de los documentos generados
DOCS_PATH = '/app/docs/_build/html/_modules/'

def extract_method_from_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        class_name = soup.find("span", class_="nc").text if soup.find("span", class_="nc") else ""
        method_name = soup.find("span", class_="fm").text if soup.find("span", class_="fm") else ""

    return class_name + "." + method_name if class_name else method_name

# Función para recopilar datos de documentos
def recopilar_datos_documentos():
    data = []

    # Lista todos los módulos
    modulos = ['administracion', 'roles', 'publicaciones', 'login', 'kanban']
    
    for modulo in modulos:
        ruta_modulo = os.path.join(DOCS_PATH, modulo)
        if os.path.exists(ruta_modulo):  # Verifica si la ruta del módulo existe
            # Lista todos los archivos en la ruta de documentos del módulo actual
            archivos = [f for f in os.listdir(ruta_modulo) if os.path.isfile(os.path.join(ruta_modulo, f)) and f.endswith('.html')]
            
            for archivo in archivos:
                file_path = os.path.join(ruta_modulo, archivo)
                fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d-%m-%Y')
                metodo = extract_method_from_html(file_path)
                data.append({
                    "SCRIPT": archivo,
                    "FECHA DOC": fecha_modificacion,
                    "MODULO": modulo,
                    "METODO": metodo,  # utiliza la función extract_method_from_html
                    "REVISADO EN SPRINT": "", 
                    "RESPONSABLE": ""
                })

    return data


# Dataframe 
df = pd.DataFrame(recopilar_datos_documentos())

# Definir el nombre del archivo
filename = "EQUIPO_06_CONTROL_DOCUMENTACION.xlsx"
df["ITEM"] = range(1, len(df) + 1)

# Las columnas 
column_order = ["ITEM", "MODULO", "SCRIPT", "METODO", "FECHA DOC", "REVISADO EN SPRINT", "RESPONSABLE"]
df = df[column_order]

with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    workbook = writer.book
    worksheet = workbook.create_sheet("Documentación de Código", 0)
    workbook.active = worksheet

    # Añadir encabezados y títulos
    worksheet.merge_cells('A1:G1')
    worksheet.cell(row=1, column=1).value = "EQUIPO NRO: 06" 

    worksheet.merge_cells('A3:G3')
    worksheet.cell(row=3, column=1).value = "PLANILLA DE CONTROL DE DOCUMENTACION DE CODIGO"

    # Escribe el DataFrame en el archivo excel
    df.to_excel(writer, sheet_name="Documentación de Código", startrow=7, index=False, header=False)
    
    # Añadir el encabezado manualmente
    headers = ["ITEM", "MODULO", "SCRIPT", "METODO", "FECHA DOC", "REVISADO EN SPRINT", "RESPONSABLE"]
    for col_num, value in enumerate(headers, 1):
        cell = worksheet.cell(row=7, column=col_num, value=value)
        cell.font = cell.font.copy(bold=True)

print(f'Archivo "{filename}" generado con éxito!')
