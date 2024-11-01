# Fast-Thumbnails

**Fast-Thumbnails** is a tool for quickly creating and customizing video thumbnails with adjustable overlay text and face positioning options. It includes a Tkinter-based configuration GUI (`gui.pyw`) for easy setup, and additional customization options can be configured via `settings.json`.

---

## Features
- Generate video thumbnails with custom text overlays, color schemes, and face positioning.
- User-friendly graphical interface for configuring settings (`gui.pyw`).
- Detailed control over text, color, and overlay filter through `settings.json`.

---

### Table of Contents
1. [Installation](#installation)
2. [Usage Examples](#usage-examples)
3. [Settings Configuration](#settings-configuration)

---

### Installation

#### Prerequisites

1. **Python 3.8 or higher** installed on your system.
2. **Tkinter** (for the GUI): You may need to install it separately on some systems. 

    ```bash
    sudo apt-get install python3-tk  # For Linux systems
    ```

3. Install dependencies listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    **Dependencies:**
    - `opencv-python`: For video and image processing.
    - `matplotlib`, `pillow`, and `numpy`: For image manipulation, rendering, and custom text adjustments.

4. **Font**: Ensure `Arial.ttf` is available for text rendering. It is included in the project but may need to be installed if unavailable on your system.

---

### Usage Examples

1. **Running the Main Script**

   To generate thumbnails, run the primary script as follows:

   ```bash
   python main.py
   ```

2. **Launching the Configuration GUI**

   To open the GUI for setting up customization options, run:

   ```bash
   python gui.pyw
   ```

   This opens the Tkinter-based interface, which allows for configuring various settings such as text color, face positioning, and overlay effects. The configurations will automatically update the `settings.json` file.

---

### Settings Configuration

The `settings.json` file contains customizable parameters for fine-tuning the appearance and behavior of thumbnails. Below is a summary of these parameters and their purposes.

```json
{
  "resolucion": [1280, 720],
  "color_texto": "#FFFF00",
  "color_contorno": "#000000",
  "tamaño_texto": 80,
  "grosor_contorno": 5,
  "posicion_texto": [50, 500],
  "limite_ancho_texto": 1000,
  "max_caras": 10,
  "posicion_cara": [770, 100],
  "fuente": "Arial.ttf",
  "tamaño_cara": "vertical",
  "filtro": {
    "activo": true,
    "tipo": "degradado",
    "color_primario": "#000000",
    "color_secundario": "#0FF000",
    "opacidad": 0.5,
    "direccion": "vertical"
  },
  "video_predeterminado": "./video.mp4",
  "carpeta_salida": "./miniaturas",
  "configuracion_parte": {
    "posicion": [50, 50],
    "tamaño": 40,
    "color": "#FFFF00"
  }
}
```

#### Configuration Options:

| Parameter                 | Description                                       | Example Value          |
|---------------------------|---------------------------------------------------|-------------------------|
| **resolucion**            | Output resolution for generated thumbnails        | `[1280, 720]`          |
| **color_texto**           | Text overlay color in hex                         | `"#FFFF00"`            |
| **color_contorno**        | Text border color in hex                          | `"#000000"`            |
| **tamaño_texto**          | Text size in pixels                               | `80`                   |
| **grosor_contorno**       | Border thickness for text in pixels               | `5`                    |
| **posicion_texto**        | Text position (x, y) on the thumbnail             | `[50, 500]`            |
| **limite_ancho_texto**    | Maximum width for text wrapping                   | `1000`                 |
| **max_caras**             | Maximum number of faces to detect and position    | `10`                   |
| **posicion_cara**         | Position to place detected faces (x, y)           | `[770, 100]`           |
| **fuente**                | Font file for text rendering                      | `"Arial.ttf"`          |
| **tamaño_cara**           | Resizing mode for detected faces                  | `"vertical"`           |
| **filtro**                | Dictionary for overlay filter settings            | See details below      |
| **video_predeterminado**  | Default video file path                           | `"./video.mp4"`        |
| **carpeta_salida**        | Directory for saving generated thumbnails         | `"./miniaturas"`       |

##### Filter (`filtro`) Settings:
- **activo**: Enable or disable the filter overlay (`true`/`false`).
- **tipo**: Filter type, e.g., `"degradado"` for a gradient overlay.
- **color_primario** and **color_secundario**: Primary and secondary colors for the gradient.
- **opacidad**: Filter opacity level, between `0` and `1`.
- **direccion**: Gradient direction (`"vertical"`, `"horizontal"`, etc.).

### Usage Examples

1. **Running the Main Script**

   To generate thumbnails, run the primary script with the required and optional parameters as follows:

   ```bash
   python main.py -t "sample text" -p 2 -i /path/to/video/examplevideo.mp4 -o /path/to/output/directory
   ```

   - `-t` (required): The text to overlay on the thumbnail.
   - `-p` (optional): The part of the video to use for the thumbnail.
   - `-i` (optional): The input video file path.
   - `-o` (optional): The output directory for saving the generated thumbnails.

   Example with only the required text parameter:

   ```bash
   python main.py -t "sample text"
   ```

2. **Launching the Configuration GUI**

   To open the GUI for setting up customization options, run:

   ```bash
   python gui.pyw
   ```

   This opens the Tkinter-based interface, which allows for configuring various settings such as text color, face positioning, and overlay effects. The configurations will automatically update the settings.json file.