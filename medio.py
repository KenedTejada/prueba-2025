import pandas as pd
import json
import sys

def cargar_reglas(archivo_json):
    """ Carga las reglas de transformación desde un archivo JSON. """
    with open(archivo_json, 'r', encoding='utf-8') as file:
        reglas = json.load(file)
    return {regla["nombre"]: regla for regla in reglas}

def transformar_excel_a_txt(input_excel, reglas_json, output_txt):
    try:
        # Cargar reglas desde JSON
        reglas = cargar_reglas(reglas_json)

        # Leer el archivo Excel y asegurarse de que todas las columnas sean strings
        df = pd.read_excel(input_excel, dtype=str).fillna('')  

        # Aplicar reglas de transformación
        for columna, regla in reglas.items():
            tamano = regla["TAMANO"]
            tipo = regla["tipo"]

            if tipo == "NUMERICO":
                df[columna] = df[columna].astype(str).str.replace('.0', '', regex=False).str.zfill(tamano)
            elif tipo == "ALFANUMERICO":
                df[columna] = df[columna].astype(str).str.ljust(tamano, '$')

        # Generar las líneas del archivo .txt
        lineas = df.apply(lambda row: ''.join(map(str, row)), axis=1)

        # Guardar en el archivo de salida
        with open(output_txt, 'w', encoding='utf-8') as file:
            file.write("\n".join(lineas))

        print(f"Archivo '{output_txt}' generado con éxito.")

    except Exception as e:
        print(f"Error: {e}")

# Ejecutar desde la terminal con argumentos
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python medio.py archivo_entrada.xlsx reglas.json archivo_salida.txt")
    else:
        transformar_excel_a_txt(sys.argv[1], sys.argv[2], sys.argv[3])
