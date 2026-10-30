"""
Conversor de HEIC a JPEG/PNG
Aplicación Streamlit para convertir imágenes HEIC/HEIF a formatos comunes.
"""

import io
import zipfile
from pathlib import Path

import streamlit as st
from PIL import Image, ImageOps

# Registrar el soporte para HEIC/HEIF en Pillow
try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
    HEIF_OK = True
except Exception:  # pragma: no cover
    HEIF_OK = False


st.set_page_config(
    page_title="Conversor HEIC → JPEG/PNG",
    page_icon="🖼️",
    layout="centered",
)

st.title("🖼️ Conversor HEIC → JPEG / PNG")
st.caption(
    "Sube una o varias imágenes `.heic` / `.heif` y conviértelas a JPEG o PNG. "
    "Las imágenes se procesan en memoria y no se guardan en ningún servidor."
)

if not HEIF_OK:
    st.error(
        "No se pudo cargar el soporte HEIC (pillow-heif). "
        "Asegúrate de que `pillow-heif` esté instalado."
    )
    st.stop()


# --- Opciones de conversión -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    output_format = st.selectbox(
        "Formato de salida",
        options=["JPEG", "PNG"],
        index=0,
    )

with col2:
    quality = st.slider(
        "Calidad (solo JPEG)",
        min_value=1,
        max_value=100,
        value=90,
        disabled=(output_format != "JPEG"),
    )

force_horizontal = st.checkbox(
    "Poner todas las fotos en horizontal (girar las verticales)",
    value=True,
    help=(
        "Primero corrige la orientación según los metadatos de la foto. "
        "Luego, cualquier imagen vertical (más alta que ancha) se gira 90° "
        "para dejarla apaisada."
    ),
)


uploaded_files = st.file_uploader(
    "Selecciona tus archivos HEIC/HEIF",
    type=["heic", "heif", "HEIC", "HEIF"],
    accept_multiple_files=True,
)


def convert_image(file, fmt: str, jpeg_quality: int, horizontal: bool) -> bytes:
    """Convierte un archivo subido a los bytes del formato indicado."""
    image = Image.open(file)

    # Aplicar la orientación guardada en EXIF para que la foto quede "derecha".
    image = ImageOps.exif_transpose(image)

    # Si se pide, girar las verticales para que queden horizontales.
    if horizontal and image.height > image.width:
        image = image.rotate(-90, expand=True)

    save_kwargs = {}
    if fmt == "JPEG":
        # JPEG no soporta transparencia -> convertir a RGB
        if image.mode in ("RGBA", "P", "LA"):
            image = image.convert("RGB")
        save_kwargs = {"quality": jpeg_quality, "optimize": True}

    buffer = io.BytesIO()
    image.save(buffer, format=fmt, **save_kwargs)
    buffer.seek(0)
    return buffer.getvalue()


if uploaded_files:
    ext = "jpg" if output_format == "JPEG" else "png"
    mime = "image/jpeg" if output_format == "JPEG" else "image/png"

    results = []  # (nombre_salida, bytes)
    errors = []

    progress = st.progress(0.0, text="Convirtiendo...")
    total = len(uploaded_files)

    for i, file in enumerate(uploaded_files, start=1):
        try:
            data = convert_image(file, output_format, quality, force_horizontal)
            out_name = f"{Path(file.name).stem}.{ext}"
            results.append((out_name, data))
        except Exception as exc:  # noqa: BLE001
            errors.append((file.name, str(exc)))
        progress.progress(i / total, text=f"Convirtiendo... ({i}/{total})")

    progress.empty()

    if errors:
        for name, msg in errors:
            st.warning(f"No se pudo convertir **{name}**: {msg}")

    if results:
        st.success(f"✅ {len(results)} imagen(es) convertida(s) a {output_format}.")

        # Vista previa + descarga individual
        for out_name, data in results:
            with st.expander(f"📄 {out_name}", expanded=(len(results) == 1)):
                st.image(data, use_container_width=True)
                st.download_button(
                    label=f"⬇️ Descargar {out_name}",
                    data=data,
                    file_name=out_name,
                    mime=mime,
                    key=f"dl_{out_name}",
                )

        # Descarga de todas en un ZIP (si hay más de una)
        if len(results) > 1:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for out_name, data in results:
                    zf.writestr(out_name, data)
            zip_buffer.seek(0)

            st.download_button(
                label="⬇️ Descargar TODAS (.zip)",
                data=zip_buffer.getvalue(),
                file_name=f"imagenes_convertidas_{ext}.zip",
                mime="application/zip",
            )
else:
    st.info("👆 Sube al menos un archivo HEIC/HEIF para empezar.")
