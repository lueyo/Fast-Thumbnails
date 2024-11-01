import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import json

# Load configuration from JSON file
with open('settings.json', 'r') as file:
    config = json.load(file)

def save_config():
    config['resolucion'] = [int(res_width.get()), int(res_height.get())]
    config['color_texto'] = text_color.get()
    config['color_contorno'] = outline_color.get()
    config['tamaño_texto'] = int(text_size.get())
    config['grosor_contorno'] = int(outline_thickness.get())
    config['posicion_texto'] = [int(text_pos_x.get()), int(text_pos_y.get())]
    config['limite_ancho_texto'] = int(text_width_limit.get())
    config['max_caras'] = int(max_faces.get())
    config['posicion_cara'] = [int(face_pos_x.get()), int(face_pos_y.get())]
    config['fuente'] = font.get()
    config['tamaño_cara'] = face_size.get()
    config['filtro']['activo'] = filter_active.get()
    config['filtro']['tipo'] = filter_type.get()
    config['filtro']['color_primario'] = primary_color.get()
    config['filtro']['color_secundario'] = secondary_color.get()
    config['filtro']['opacidad'] = float(filter_opacity.get())
    config['filtro']['direccion'] = filter_direction.get()
    config['video_predeterminado'] = default_video.get()
    config['carpeta_salida'] = output_folder.get()
    config['configuracion_parte']['posicion'] = [int(part_pos_x.get()), int(part_pos_y.get())]
    config['configuracion_parte']['tamaño'] = int(part_size.get())
    config['configuracion_parte']['color'] = part_color.get()

    with open('settings.json', 'w') as file:
        json.dump(config, file, indent=4)

# Create main window
root = tk.Tk()
root.title("Configuración")

# Create widgets
res_width = tk.Entry(root)
res_height = tk.Entry(root)
text_color = tk.Entry(root)
outline_color = tk.Entry(root)
text_size = tk.Entry(root)
outline_thickness = tk.Entry(root)
text_pos_x = tk.Entry(root)
text_pos_y = tk.Entry(root)
text_width_limit = tk.Entry(root)
max_faces = tk.Entry(root)
face_pos_x = tk.Entry(root)
face_pos_y = tk.Entry(root)
font = tk.Entry(root)
face_size = tk.Entry(root)
filter_active = tk.BooleanVar()
filter_active_check = tk.Checkbutton(root, variable=filter_active)
filter_type = tk.Entry(root)
primary_color = tk.Entry(root)
secondary_color = tk.Entry(root)
filter_opacity = tk.Entry(root)
filter_direction = tk.Entry(root)
default_video = tk.Entry(root)
output_folder = tk.Entry(root)
part_pos_x = tk.Entry(root)
part_pos_y = tk.Entry(root)
part_size = tk.Entry(root)
part_color = tk.Entry(root)

# Set default values
res_width.insert(0, config['resolucion'][0])
res_height.insert(0, config['resolucion'][1])
text_color.insert(0, config['color_texto'])
outline_color.insert(0, config['color_contorno'])
text_size.insert(0, config['tamaño_texto'])
outline_thickness.insert(0, config['grosor_contorno'])
text_pos_x.insert(0, config['posicion_texto'][0])
text_pos_y.insert(0, config['posicion_texto'][1])
text_width_limit.insert(0, config['limite_ancho_texto'])
max_faces.insert(0, config['max_caras'])
face_pos_x.insert(0, config['posicion_cara'][0])
face_pos_y.insert(0, config['posicion_cara'][1])
font.insert(0, config['fuente'])
face_size.insert(0, config['tamaño_cara'])
filter_active.set(config['filtro']['activo'])
filter_type.insert(0, config['filtro']['tipo'])
primary_color.insert(0, config['filtro']['color_primario'])
secondary_color.insert(0, config['filtro']['color_secundario'])
filter_opacity.insert(0, config['filtro']['opacidad'])
filter_direction.insert(0, config['filtro']['direccion'])
default_video.insert(0, config['video_predeterminado'])
output_folder.insert(0, config['carpeta_salida'])
part_pos_x.insert(0, config['configuracion_parte']['posicion'][0])
part_pos_y.insert(0, config['configuracion_parte']['posicion'][1])
part_size.insert(0, config['configuracion_parte']['tamaño'])
part_color.insert(0, config['configuracion_parte']['color'])

# Layout management
labels = [
    "Resolución (Ancho x Alto)", "Color del Texto", "Color del Contorno", "Tamaño del Texto",
    "Grosor del Contorno", "Posición del Texto (X, Y)", "Límite de Ancho del Texto", "Máximo de Caras",
    "Posición de la Cara (X, Y)", "Fuente", "Tamaño de la Cara", "Filtro Activo", "Tipo de Filtro",
    "Color Primario del Filtro", "Color Secundario del Filtro", "Opacidad del Filtro", "Dirección del Filtro",
    "Video Predeterminado", "Carpeta de Salida", "Posición de la Parte (X, Y)", "Tamaño de la Parte", "Color de la Parte"
]

entries = [
    (res_width, res_height), text_color, outline_color, text_size, outline_thickness,
    (text_pos_x, text_pos_y), text_width_limit, max_faces, (face_pos_x, face_pos_y), font,
    face_size, filter_active_check, filter_type, primary_color, secondary_color, filter_opacity,
    filter_direction, default_video, output_folder, (part_pos_x, part_pos_y), part_size, part_color
]

for i, (label, entry) in enumerate(zip(labels, entries)):
    tk.Label(root, text=label).grid(row=i, column=0, sticky='w')
    if isinstance(entry, tuple):
        for j, sub_entry in enumerate(entry):
            sub_entry.grid(row=i, column=j+1)
    else:
        entry.grid(row=i, column=1)

# Save button
save_button = tk.Button(root, text="Guardar", command=save_config)
save_button.grid(row=len(labels), column=0, columnspan=2)

# Run main loop
root.mainloop()