 
from odoo import models, fields, api
import pandas as pd
import json
import base64
import tempfile

class TransformadorArchivo(models.Model):
    _name = 'transformador.archivo'
    _description = 'Transformador de Archivos'

    name = fields.Char(string="Nombre del archivo")
    excel_file = fields.Binary(string="Archivo Excel", attachment=True)
    txt_file = fields.Binary(string="Archivo Transformado", readonly=True)
    txt_filename = fields.Char(string="Nombre del Archivo TXT")

    def transformar_archivo(self):
        """ Método que toma el Excel, aplica las reglas y genera un TXT """
        if not self.excel_file:
            return
        
        reglas = json.load(open('/ruta/del/archivo/reglas.json'))  # Ajustar ruta

        # Convertir archivo binario a Excel
        excel_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        with open(excel_path, "wb") as f:
            f.write(base64.b64decode(self.excel_file))

        df = pd.read_excel(excel_path, dtype=str).fillna('')

        # Aplicar reglas
        for regla in reglas:
            columna = regla["nombre"]
            tamano = regla["TAMANO"]
            if regla["tipo"] == "NUMERICO":
                df[columna] = df[columna].astype(str).str.zfill(tamano)
            else:
                df[columna] = df[columna].astype(str).str.ljust(tamano, '$')

        # Guardar en archivo TXT
        txt_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name
        df.to_csv(txt_path, index=False, header=False)

        # Convertir a binario para Odoo
        with open(txt_path, "rb") as f:
            txt_data = f.read()
            self.txt_file = base64.b64encode(txt_data)
            self.txt_filename = "archivo_salida.txt"
