import zipfile
import json
import os
import sys
import re
import html
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def extraer_h5p(ruta_h5p, destino):
    """Descomprime el paquete H5P como si fuera un ZIP"""
    with zipfile.ZipFile(ruta_h5p, 'r') as zip_ref:
        zip_ref.extractall(destino)

def limpiar_html(texto_html):
    """Limpia etiquetas HTML y estilos complejos que rompen ReportLab"""
    if not texto_html:
        return ""
    # 1. Reemplazar cierres de párrafo, saltos de línea y listas con un espacio para no juntar palabras
    texto = re.sub(r'<(br|/p|/div|/h[1-6]|/li)>', ' ', texto_html, flags=re.IGNORECASE)
    # 2. Borrar cualquier otra etiqueta HTML (como span, strong, etc.)
    texto = re.sub(r'<[^>]+>', '', texto)
    # 3. Convertir entidades HTML (como &aacute; a á)
    texto = html.unescape(texto)
    # 4. Limpiar espacios extra
    return re.sub(r'\s+', ' ', texto).strip()

def recorrer_json_y_extraer_texto(data, lista_elementos, carpeta_content):
    """Recorre recursivamente la estructura JSON de H5P buscando textos e imágenes"""
    if isinstance(data, dict):
        if 'params' in data and isinstance(data['params'], dict):
            params = data['params']
            
            # Extraer bloques de texto y limpiarlos
            if 'text' in params and isinstance(params['text'], str):
                texto_limpio = limpiar_html(params['text'])
                if texto_limpio:
                    lista_elementos.append(('texto', texto_limpio))
            
            # Extraer imágenes
            if 'file' in params and isinstance(params['file'], dict):
                path_img = params['file'].get('path')
                if path_img:
                    full_path = os.path.join(carpeta_content, path_img)
                    if os.path.exists(full_path):
                        lista_elementos.append(('imagen', full_path))
                        
        for key, value in data.items():
            recorrer_json_y_extraer_texto(value, lista_elementos, carpeta_content)
            
    elif isinstance(data, list):
        for item in data:
            recorrer_json_y_extraer_texto(item, lista_elementos, carpeta_content)

def generar_pdf(elementos, archivo_salida):
    """Construye el PDF final maquetado"""
    doc = SimpleDocTemplate(archivo_salida, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el texto
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        spaceAfter=10
    )

    story = []
    
    titulo_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#1A5276'), spaceAfter=20)
    story.append(Paragraph("<b>Material de Estudio Offline</b>", titulo_style))
    story.append(Spacer(1, 15))

    for tipo, contenido in elementos:
        if tipo == 'texto':
            try:
                p = Paragraph(contenido, body_style)
                story.append(p)
                story.append(Spacer(1, 8))
            except Exception as e:
                print(f"Omitiendo bloque de texto problemático: {e}")
            
        elif tipo == 'imagen':
            try:
                img = Image(contenido, width=450, height=250)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 15))
            except Exception as e:
                print(f"No se pudo procesar la imagen {contenido}: {e}")

    doc.build(story)
    print(f"\n¡PDF generado con éxito!: {archivo_salida}")

# === EJECUCIÓN DEL PROCESO ===
if __name__ == "__main__":
    # Verificar que se haya pasado un argumento por línea de comandos
    if len(sys.argv) < 2:
        print("Error: Debes indicar el nombre del archivo .h5p.")
        print("Uso correcto: python h5p_a_pdf.py nombre_del_archivo.h5p")
        sys.exit(1)

    archivo_h5p = sys.argv[1]

    # Verificar que el archivo exista
    if not os.path.exists(archivo_h5p):
        print(f"Error: No se encuentra el archivo '{archivo_h5p}'.")
        sys.exit(1)

    # Generar nombres dinámicos basados en el archivo de entrada
    nombre_base = os.path.splitext(os.path.basename(archivo_h5p))[0]
    output_pdf = os.path.join("out", f"{nombre_base}.pdf")
    carpeta_extraccion = f"temp_{nombre_base}"

    # Asegurar que exista la carpeta de salida
    os.makedirs("out", exist_ok=True)

    print(f"1. Descomprimiendo el archivo '{archivo_h5p}'...")
    extraer_h5p(archivo_h5p, carpeta_extraccion)

    ruta_json = os.path.join(carpeta_extraccion, 'content', 'content.json')
    carpeta_content = os.path.join(carpeta_extraccion, 'content')

    if os.path.exists(ruta_json):
        print("2. Leyendo, limpiando y extrayendo el contenido del curso...")
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos_curso = json.load(f)

        elementos_extraidos = []
        recorrer_json_y_extraer_texto(datos_curso, elementos_extraidos, carpeta_content)

        print("3. Generando el documento PDF...")
        generar_pdf(elementos_extraidos, output_pdf)
        
        # Limpiar la carpeta temporal
        print("4. Limpiando archivos temporales...")
        shutil.rmtree(carpeta_extraccion)
        print("¡Proceso finalizado!")
    else:
        print("Error: No se encontró la estructura de contenido dentro del paquete H5P.")
        shutil.rmtree(carpeta_extraccion)
