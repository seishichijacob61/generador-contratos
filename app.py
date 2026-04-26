import streamlit as st
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os

st.set_page_config(page_title="Generador de Contratos", layout="centered")

st.title("📄 Generador de Contrato de Evento")

# =========================
# RUTA BASE
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================
# ARRENDADOR
# =========================
st.subheader("🏢 Datos del Arrendador")
arrendador_nombre = st.text_input("Nombre del arrendador")
tipo_doc_arrendador = st.selectbox("Tipo doc arrendador", ["DNI", "RUC", "Otro"])
arrendador_doc = st.text_input("Número documento")
arrendador_direccion = st.text_input("Dirección")

# =========================
# CLIENTE
# =========================
st.subheader("👤 Datos del Cliente")
arrendatario_nombre = st.text_input("Nombre cliente")
tipo_doc = st.selectbox("Tipo doc cliente", ["DNI", "Carnet de Extranjería", "Pasaporte", "Otro"])
arrendatario_doc = st.text_input("Número documento cliente")
arrendatario_direccion = st.text_input("Dirección cliente")

# =========================
# EVENTO
# =========================
st.subheader("📅 Datos del Evento")
direccion_local = st.text_input("Dirección del local")

fecha_inicio = st.date_input("Fecha inicio")
hora_inicio = st.time_input("Hora inicio")

fecha_fin = st.date_input("Fecha fin")
hora_fin = st.time_input("Hora fin")

# =========================
# PAGOS
# =========================
st.subheader("💰 Pagos")
monto_total = st.number_input("Monto total", min_value=0.0)
adelanto = st.number_input("Adelanto", min_value=0.0)
saldo = monto_total - adelanto
fecha_pago = st.date_input("Fecha adelanto")

# =========================
# LEGAL
# =========================
st.subheader("⚖️ Legal")
jurisdiccion = st.text_input("Jurisdicción")
lugar_fecha = st.text_input("Lugar y fecha firma")

# =========================
# GENERAR
# =========================
if st.button("📄 Generar contrato"):

    try:
        env = Environment(loader=FileSystemLoader(BASE_DIR))
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

            fecha_inicio=fecha_inicio.strftime("%d/%m/%Y") if fecha_inicio else "",
            hora_inicio=str(hora_inicio),
            fecha_fin=fecha_fin.strftime("%d/%m/%Y") if fecha_fin else "",
            hora_fin=str(hora_fin),

            monto_total=monto_total,
            adelanto=adelanto,
            saldo=saldo,
            fecha_pago=fecha_pago.strftime("%d/%m/%Y") if fecha_pago else "",

            jurisdiccion=jurisdiccion,
            lugar_fecha=lugar_fecha
        )

        # Guardar HTML
        html_path = os.path.join(BASE_DIR, "contrato.html")
        pdf_path = os.path.join(BASE_DIR, "contrato.pdf")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Generar PDF
        with open(html_path, "r", encoding="utf-8") as f:
            source_html = f.read()

        with open(pdf_path, "wb") as output_file:
            pisa_status = pisa.CreatePDF(source_html, dest=output_file)

        if pisa_status.err:
            st.error("❌ Error generando PDF")
        else:
            st.success("✅ Contrato generado")

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Descargar PDF",
                    data=f,
                    file_name="contrato_evento.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error(f"❌ Error general: {e}")