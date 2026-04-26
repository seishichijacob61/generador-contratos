import streamlit as st
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os

st.set_page_config(page_title="Generador de Contratos", layout="centered")

st.title("📄 Generador de Contrato de Evento")

# =========================
# ARRENDADOR
# =========================
st.subheader("🏢 Datos del Arrendador")
arrendador_nombre = st.text_input("Nombre del arrendador")
tipo_doc_arrendador = st.selectbox(
    "Tipo de documento arrendador",
    ["DNI", "RUC", "Otro"]
)
arrendador_doc = st.text_input("Número de documento")
arrendador_direccion = st.text_input("Dirección del arrendador")

# =========================
# CLIENTE
# =========================
st.subheader("👤 Datos del Cliente")
arrendatario_nombre = st.text_input("Nombre del cliente")
tipo_doc = st.selectbox(
    "Tipo de documento cliente",
    ["DNI", "Carnet de Extranjería", "Pasaporte", "Otro"]
)
arrendatario_doc = st.text_input("Número de documento cliente")
arrendatario_direccion = st.text_input("Dirección del cliente")

# =========================
# EVENTO
# =========================
st.subheader("📅 Datos del Evento")
direccion_local = st.text_input("Dirección del local")

fecha_inicio = st.date_input("Fecha de inicio")
hora_inicio = st.time_input("Hora de inicio")

fecha_fin = st.date_input("Fecha de fin")
hora_fin = st.time_input("Hora de término")

# =========================
# PAGOS
# =========================
st.subheader("💰 Datos de Pago")
monto_total = st.number_input("Monto total", min_value=0.0, step=50.0)
adelanto = st.number_input("Monto de separación", min_value=0.0, step=50.0)

saldo = monto_total - adelanto
fecha_pago = st.date_input("Fecha del adelanto")

# =========================
# LEGAL
# =========================
st.subheader("⚖️ Datos Legales")
jurisdiccion = st.text_input("Ciudad de jurisdicción")
lugar_fecha = st.text_input("Lugar y fecha de firma")

# =========================
# GENERAR CONTRATO
# =========================
if st.button("📄 Generar contrato"):

    ruta = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(ruta))
    template = env.get_template("contrato_template.html")

    html = template.render(
        arrendador_nombre=arrendador_nombre,
        tipo_doc_arrendador=tipo_doc_arrendador,
        arrendador_doc=arrendador_doc,
        arrendador_direccion=arrendador_direccion,

        arrendatario_nombre=arrendatario_nombre,
        tipo_documento=tipo_doc,
        arrendatario_documento=arrendatario_doc,
        arrendatario_direccion=arrendatario_direccion,

        direccion_local=direccion_local,

        fecha_inicio=fecha_inicio.strftime("%d/%m/%Y"),
        hora_inicio=str(hora_inicio),
        fecha_fin=fecha_fin.strftime("%d/%m/%Y"),
        hora_fin=str(hora_fin),

        monto_total=monto_total,
        adelanto=adelanto,
        saldo=saldo,
        fecha_pago=fecha_pago.strftime("%d/%m/%Y"),

        jurisdiccion=jurisdiccion,
        lugar_fecha=lugar_fecha
    )

    with open("contrato.html", "w", encoding="utf-8") as f:
        f.write(html)

    with open("contrato.html", "r", encoding="utf-8") as f:
        source_html = f.read()

    with open("contrato.pdf", "wb") as output_file:
        pisa_status = pisa.CreatePDF(source_html, dest=output_file)

    if pisa_status.err:
        st.error("Error al generar PDF")
    else:
        st.success("✅ Contrato generado correctamente")

        with open("contrato.pdf", "rb") as f:
            st.download_button(
                label="📥 Descargar PDF",
                data=f,
                file_name="contrato_evento.pdf",
                mime="application/pdf"
            )