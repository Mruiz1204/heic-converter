# 🖼️ Conversor HEIC → JPEG / PNG

Aplicación web hecha con [Streamlit](https://streamlit.io) para convertir imágenes
`.heic` / `.heif` (el formato de fotos de iPhone) a **JPEG** o **PNG**.

- Sube una o varias imágenes a la vez.
- Elige el formato de salida (JPEG o PNG) y la calidad del JPEG.
- Descarga cada imagen por separado o todas juntas en un `.zip`.
- Las imágenes se procesan en memoria: no se guardan en ningún servidor.

## 🚀 Probar en local

Necesitas Python 3.9 o superior.

```bash
# 1. Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py
```

Se abrirá en el navegador en `http://localhost:8501`.

## ☁️ Desplegar en Streamlit Community Cloud

1. Sube este proyecto a un repositorio de **GitHub** (ver abajo).
2. Entra en [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.
3. Pulsa **"New app"**, elige tu repositorio, la rama (`main`) y el archivo principal `app.py`.
4. Pulsa **Deploy**. Streamlit instalará las dependencias de `requirements.txt` automáticamente.

## 📁 Estructura del proyecto

```
heic-converter/
├── app.py              # Aplicación Streamlit
├── requirements.txt    # Dependencias
├── .gitignore
├── .streamlit/
│   └── config.toml     # Configuración (tamaño máximo de subida, tema)
└── README.md
```

## 🔧 Tecnologías

- **Streamlit** – interfaz web
- **Pillow** – manejo de imágenes
- **pillow-heif** – decodificación de HEIC/HEIF
