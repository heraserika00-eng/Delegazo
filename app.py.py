import streamlit as st
import qrcode
from PIL import Image
import io
import uuid

st.title("🎟️ Compra de Entradas - Halloween Sangriento by Delegazo MC")

# Formulario de Compra
with st.form("compra_form"):
    nombre = st.text_input("Nombre y Apellido")
    cedula = st.text_input("Cédula ")
    celular = st.text_input("número de celular")
    comprar = st.form_submit_button("Generar Entrada")

if comprar and nombre and cedula:
    # Crear un ID único para la entrada
    id_ticket = str(uuid.uuid4())[:8]
    
    # URL o Datos que tendrá el QR al escanear
    # En producción sustituyes por la URL de tu página web
    contenido_qr = f"ID: {id_ticket}\nNombre: {nombre}\nCedula: {cedula}\nEstado: VALIDA"
    
    # Generar Imagen QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(contenido_qr)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir para mostrar en la web
    buf = io.BytesIO()
    img_qr.save(buf)
    
    st.success(f"¡Entrada generada con éxito para {nombre}!")
    st.image(buf, caption=f"Tu Código QR (ID: {id_ticket})", width=250)
