import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime

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
fecha_evento = st.date_input("Fecha del evento")
hora_inicio = st.time_input("Hora de inicio")
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

    styles = getSampleStyleSheet()
    contenido = []

    def add(text):
        contenido.append(Paragraph(text, styles["Normal"]))
        contenido.append(Spacer(1, 8))

    # =========================
    # CONTENIDO DEL CONTRATO
    # =========================
    add("<b>CONTRATO DE ALQUILER DE LOCAL PARA EVENTO</b>")

    add(f"EL ARRENDADOR: {arrendador_nombre}, identificado con {tipo_doc_arrendador} N° {arrendador_doc}, con domicilio en {arrendador_direccion}.")
    add(f"EL ARRENDATARIO: {arrendatario_nombre}, identificado con {tipo_doc} N° {arrendatario_doc}, con domicilio en {arrendatario_direccion}.")

    add("<b>PRIMERA: OBJETO DEL CONTRATO</b>")
    add(f"El local ubicado en {direccion_local} será utilizado para un evento privado.")

    add("<b>SEGUNDA: FECHA Y HORARIO</b>")
    add(f"Fecha: {fecha_evento.strftime('%d/%m/%Y')}")
    add(f"Inicio: {hora_inicio} - Fin: {hora_fin}")

    add("<b>TERCERA: PRECIO</b>")
    add(f"Monto total: S/ {monto_total}")
    add(f"Adelanto: S/ {adelanto} ({fecha_pago.strftime('%d/%m/%Y')})")
    add(f"Saldo: S/ {saldo}")

    add("<b>CUARTA: USO DEL LOCAL</b>")
    add("No subarrendar, no exceder capacidad, no actividades ilícitas.")

    add("<b>QUINTA: RUIDOS</b>")
    add("El arrendatario respetará niveles de ruido.")

    add("<b>SEXTA: DAÑOS</b>")
    add("Responsable por daños ocasionados.")

    add("<b>SÉPTIMA: SEGURIDAD</b>")
    add("Responsabilidad del arrendatario.")

    add("<b>OCTAVA: CANCELACIÓN</b>")
    add("No devolución si cancela el arrendatario.")

    add("<b>NOVENA: MODIFICACIONES</b>")
    add("Toda modificación debe ser por escrito.")

    add("<b>DÉCIMA: JURISDICCIÓN</b>")
    add(f"Jurisdicción: {jurisdiccion}")

    add(f"Lugar y fecha: {lugar_fecha}")

    add(" ")
    add("EL ARRENDADOR ______________________")
    add("EL ARRENDATARIO ______________________")

    # =========================
    # CREAR PDF
    # =========================
    pdf_file = "contrato.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    doc.build(contenido)

    st.success("✅ Contrato generado correctamente")

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📥 Descargar PDF",
            data=f,
            file_name="contrato_evento.pdf",
            mime="application/pdf"
        )