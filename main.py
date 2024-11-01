import json
import random
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import cv2
import datetime
# Cargar configuración desde settings.json
with open('settings.json', 'r') as f:
    settings = json.load(f)

# Parámetros básicos desde settings.json
RESOLUCION = tuple(settings["resolucion"])
COLOR_TEXTO = settings["color_texto"]
COLOR_CONTORNO = settings["color_contorno"]
TAMANO_TEXTO = settings["tamaño_texto"]
GROSOR_CONTORNO = settings["grosor_contorno"]
POSICION_TEXTO = tuple(settings["posicion_texto"])
LIMITE_ANCHO_TEXTO = settings["limite_ancho_texto"]
MAX_CARAS = settings["max_caras"]
POSICION_CARA = tuple(settings["posicion_cara"])
FUENTE = settings["fuente"]
FILTRO = settings["filtro"]
VIDEO_PRED = settings["video_predeterminado"]
CARPETA_SALIDA = settings["carpeta_salida"]

# Configuración para la etiqueta "parte"
POSICION_PARTE = tuple(settings["configuracion_parte"]["posicion"])
TAMANO_PARTE = settings["configuracion_parte"]["tamaño"]
COLOR_PARTE = settings["configuracion_parte"]["color"]


# Obtener argumentos de entrada para el texto y otros parámetros
texto = ""
parte = None
input_path = VIDEO_PRED
output_dir = CARPETA_SALIDA

def aplicar_filtro(imagen):
    overlay = Image.new("RGBA", imagen.size)
    draw = ImageDraw.Draw(overlay)
    
    if FILTRO["activo"]:
        color1 = FILTRO["color_primario"] + hex(int(FILTRO["opacidad"] * 255))[2:]
        
        if FILTRO["tipo"] == "color_sólido":
            draw.rectangle([(0, 0), imagen.size], fill=color1)
        elif FILTRO["tipo"] == "sombra":
            draw.rectangle([(0, 0), imagen.size], fill=color1)
        elif FILTRO["tipo"] == "degradado":
            color2 = FILTRO["color_secundario"] + hex(int(FILTRO["opacidad"] * 255))[2:]
            if FILTRO["direccion"] == "vertical":
                for y in range(imagen.height):
                    alpha = y / imagen.height
                    color = Image.blend(Image.new("RGBA", (1, 1), color1),
                                        Image.new("RGBA", (1, 1), color2), alpha).getpixel((0, 0))
                    draw.line([(0, y), (imagen.width, y)], fill=color)
            elif FILTRO["direccion"] == "horizontal":
                for x in range(imagen.width):
                    alpha = x / imagen.width
                    color = Image.blend(Image.new("RGBA", (1, 1), color1),
                                        Image.new("RGBA", (1, 1), color2), alpha).getpixel((0, 0))
                    draw.line([(x, 0), (x, imagen.height)], fill=color)
    
    return Image.alpha_composite(imagen.convert("RGBA"), overlay)

for i in range(len(sys.argv)):
    if sys.argv[i] == "-t" and i + 1 < len(sys.argv):
        texto = sys.argv[i + 1]
    elif sys.argv[i] == "-p" and i + 1 < len(sys.argv):
        parte = sys.argv[i + 1]
    elif sys.argv[i] == "-i" and i + 1 < len(sys.argv):
        input_path = sys.argv[i + 1]
    elif sys.argv[i] == "-o" and i + 1 < len(sys.argv):
        output_dir = sys.argv[i + 1]

# Listar archivos en el directorio de caras
caras_dir = "./caras"
caras_files = [f for f in os.listdir(caras_dir) if os.path.isfile(os.path.join(caras_dir, f))]
num_caras_disponibles = len(caras_files)
num_caras_a_usar = min(5, MAX_CARAS, num_caras_disponibles)  # Asegurarse de no intentar extraer más caras de las que hay disponibles

# Seleccionar caras aleatorias
caras = [os.path.join(caras_dir, caras_files[i]) for i in random.sample(range(num_caras_disponibles), num_caras_a_usar)]

# Extraer fotogramas aleatorios del video
def extraer_fotogramas(video_path, num_frames=5):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fotogramas = []
    for _ in range(num_frames):
        frame_id = random.randint(0, total_frames - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        if ret:
            fotogramas.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return fotogramas

# Función para dibujar texto con contorno
def dibujar_texto_con_contorno(draw, posicion, texto, font, color_texto, color_contorno, grosor_contorno):
    x, y = posicion
    # Dibujar contorno
    for dx in range(-grosor_contorno, grosor_contorno + 1):
        for dy in range(-grosor_contorno, grosor_contorno + 1):
            if dx != 0 or dy != 0:  # Evitar el centro
                draw.text((x + dx, y + dy), texto, font=font, fill=color_contorno)
    # Dibujar texto principal
    draw.text((x, y), texto, font=font, fill=color_texto)

# Función para dividir texto en líneas
def dividir_texto(draw, texto, font, limite_ancho):
    """
    Divide el texto en múltiples líneas que se ajusten dentro del límite de ancho especificado.
    """
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba = linea_actual + " " + palabra if linea_actual else palabra
        if draw.textlength(prueba, font=font) <= limite_ancho:
            linea_actual = prueba
        else:
            lineas.append(linea_actual)
            linea_actual = palabra

    # Añadir la última línea
    if linea_actual:
        lineas.append(linea_actual)

    return lineas

# Función para crear una miniatura
def crear_miniatura(fondo, cara_path, texto, parte):
    fondo = Image.fromarray(fondo).resize(RESOLUCION)
    cara = Image.open(cara_path)

    # Ajuste de tamaño y posición de la cara
    if settings["tamaño_cara"] == "vertical":
        proporcion = RESOLUCION[1] / cara.height
        nuevo_ancho = int(cara.width * proporcion)
        cara = cara.resize((nuevo_ancho, RESOLUCION[1]))
    fondo = aplicar_filtro(fondo)
    fondo.paste(cara, POSICION_CARA, cara.convert("RGBA"))

    # Añadir texto principal
    draw = ImageDraw.Draw(fondo)
    font_texto = ImageFont.truetype(FUENTE, TAMANO_TEXTO)
    lineas = dividir_texto(draw, texto.upper(), font_texto, LIMITE_ANCHO_TEXTO)
    y_offset = POSICION_TEXTO[1]
    for linea in lineas:
        posicion = (POSICION_TEXTO[0], y_offset)
        dibujar_texto_con_contorno(draw, posicion, linea, font_texto, COLOR_TEXTO, COLOR_CONTORNO, GROSOR_CONTORNO)
        y_offset += TAMANO_TEXTO + 10

    # Añadir "parte" si está presente
    if parte:
        font_parte = ImageFont.truetype(FUENTE, TAMANO_PARTE)
        texto_parte = f"Parte {parte}"
        dibujar_texto_con_contorno(draw, POSICION_PARTE, texto_parte, font_parte, COLOR_PARTE, COLOR_CONTORNO, GROSOR_CONTORNO)

    return fondo

# Crear las miniaturas
fotogramas = extraer_fotogramas(input_path, 5)
os.makedirs(output_dir, exist_ok=True)
ts = str(datetime.datetime.now().timestamp())
for i, fondo in enumerate(fotogramas):
    if i < len(caras):  # Asegurarse de no exceder el número de caras disponibles
        miniatura = crear_miniatura(fondo, caras[i], texto, parte)
        miniatura.save(os.path.join(output_dir, f"{ts}_{i + 1}.png"), format="PNG")

print("Miniaturas generadas con éxito.")