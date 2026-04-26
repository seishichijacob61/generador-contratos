import streamlit as st
from jinja2 import Environment, FileSystemLoader
import base64

st.set_page_config(page_title="Generador de Contratos", layout="centered")

st.title("📄 Generador de Contrato de Evento")

# =========================
# FUNCION NUMERO A LETRAS
# =========================
def numero_a_letras(num):
    unidades = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
    especiales = ["diez", "once", "doce", "trece", "catorce", "quince"]
    decenas = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
    centenas = ["", "cien", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]

    if num == 0:
        return "cero"

    if num < 10:
        return unidades[num]

    if num < 16:
        return especiales[num - 10]

    if num < 20:
        return "dieci" + unidades[num - 10]

    if num < 100:
        d, u = divmod(num, 10)
        if u == 0:
            return decenas[d]
        return decenas[d] + " y " + unidades[u]

    if num < 1000:
        c, r = divmod(num, 100)
        if r == 0:
            return centenas[c]
        return centenas[c] + " " + numero_a_letras(r)

    return str(num)

# =========================
# FORMATO HORA AM/PM
# =========================
def formato_hora(hora):
    return hora.strftime("%I:%M %p")

# =========================
# DATOS
# =========================
st.subheader("🏢 Arrendador")
arrendador_nombre = st.text_input("Nombre")
arrendador_doc = st.selectbox("Tipo doc", ["DNI", "Carnet de Extranjería", "Pasaporte"])
arrendador_dni = st.text_input("Número")
arrendador_direccion = st.text_input("Dirección")

st.subheader("👤 Cliente")
arrendatario_nombre = st.text_input("Nombre cliente")
arrendatario_doc = st.selectbox("Tipo doc cliente", ["DNI", "Carnet de Extranjería", "Pasaporte"])
arrendatario_dni = st.text_input("Número cliente")
arrendatario_direccion = st.text_input("Dirección cliente")

st.subheader("📅 Evento")
direccion_local = st.text_input("Dirección del local")

fecha_inicio = st.date_input("Fecha inicio")
hora_inicio = st.time_input("Hora inicio")

fecha_fin = st.date_input("Fecha fin")
hora_fin = st.time_input("Hora fin")

st.subheader("💰 Pago")
monto_total = st.number_input("Monto total", min_value=0.0)
adelanto = st.number_input("Adelanto", min_value=0.0)
saldo = monto_total - adelanto
fecha_pago = st.date_input("Fecha adelanto")

st.subheader("⚖️ Legal")
jurisdiccion = st.text_input("Jurisdicción")
lugar_fecha = st.text_input("Lugar y fecha")

# =========================
# GENERAR
# =========================
if st.button("📄 Generar contrato"):

    monto_letras = numero_a_letras(int(monto_total)) + " soles"

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("contrato_template.html")

    html = template.render(
        arrendador_nombre=arrendador_nombre,
        arrendador_doc=arrendador_doc,
        arrendador_dni=arrendador_dni,
        arrendador_direccion=arrendador_direccion,

        arrendatario_nombre=arrendatario_nombre,
        arrendatario_doc=arrendatario_doc,
        arrendatario_dni=arrendatario_dni,
        arrendatario_direccion=arrendatario_direccion,

        direccion_local=direccion_local,

        fecha_inicio=fecha_inicio.strftime("%d/%m/%Y"),
        hora_inicio=formato_hora(hora_inicio),

        fecha_fin=fecha_fin.strftime("%d/%m/%Y"),
        hora_fin=formato_hora(hora_fin),

        monto_total=monto_total,
        monto_letras=monto_letras,
        adelanto=adelanto,
        saldo=saldo,
        fecha_pago=fecha_pago.strftime("%d/%m/%Y"),

        jurisdiccion=jurisdiccion,
        lugar_fecha=lugar_fecha
    )

    st.success("✅ Contrato generado")

    # MOSTRAR
    st.components.v1.html(html, height=900, scrolling=True)

    # DESCARGAR HTML (FUNCIONA EN CELULAR)
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="contrato.html">📥 Descargar contrato</a>'
    st.markdown(href, unsafe_allow_html=True)