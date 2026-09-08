import streamlit as st
import qrcode
from PIL import Image
import io
import uuid
import pandas as pd

# Configuración inicial de la página
st.set_page_config(page_title="Farra Déleg - Entradas", page_icon="🎟️")

# Estructura para guardar datos temporalmente en sesión
if "entradas" not in st.session_state:
    st.session_state["entradas"] = []

st.title("🎟️ Farra Déleg - Venta de Entradas")

# Menú superior para cambiar entre Comprador y Administrador
modo = st.sidebar.radio("Navegación", ["Comprar Entrada", "Panel de Administración"])

# ----------------------------------------------------
# VISTA 1: FORMULARIO DE COMPRA (COMPRADOR)
# ----------------------------------------------------
if modo == "Comprar Entrada":
    st.header("Solicitud de Entrada")
    st.write("Llena tus datos para solicitar tu pase al evento.")

    with st.form("form_compra"):
        nombre = st.text_input("Nombre y Apellido")
        cedula = st.text_input("Cédula / DNI")
        correo = st.text_input("Correo Electrónico")
        
        # Opciones de entradas solicitadas
        tipo_entrada = st.radio(
            "Selecciona tu tipo de entrada:",
            ["Con Disfraz 🎭", "Sin Disfraz 👕"]
        )
        
        btn_solicitar = st.form_submit_button("Enviar Solicitud")

    if btn_solicitar:
        if nombre and cedula and correo:
            ticket_id = str(uuid.uuid4())[:8]
            
            # Guardar entrada en estado PENDIENTE
            nueva_entrada = {
                "id": ticket_id,
                "nombre": nombre,
                "cedula": cedula,
                "correo": correo,
                "tipo": tipo_entrada,
                "estado": "PENDIENTE"
            }
            st.session_state["entradas"].append(nueva_entrada)
            
            st.warning("⚠️ Tu solicitud ha sido enviada. Tu código QR se generará una vez que la administración apruebe tu pago/registro.")
            st.info(f"Guarda tu ID de seguimiento: **{ticket_id}**")
        else:
            st.error("Por favor completa todos los campos del formulario.")

# ----------------------------------------------------
# VISTA 2: PANEL DE ADMINISTRACIÓN (ADMIN)
# ----------------------------------------------------
elif modo == "Panel de Administración":
    st.header("🔒 Control Administrativo")
    
    clave = st.text_input("Ingresa la clave de administrador:", type="password")
    
    # Clave de prueba simple: "admin123"
    if clave == "admin123":
        st.success("Acceso concedido.")
        
        if len(st.session_state["entradas"]) == 0:
            st.info("No hay solicitudes registradas por el momento.")
        else:
            df = pd.DataFrame(st.session_state["entradas"])
            st.subheader("Lista de Solicitudes")
            st.dataframe(df[["id", "nombre", "cedula", "tipo", "estado"]])
            
            st.divider()
            st.subheader("Aprobar Entradas")
            
            # Filtrar entradas pendientes de aprobación
            pendientes = [e for e in st.session_state["entradas"] if e["estado"] == "PENDIENTE"]
            
            if pendientes:
                for entrada in pendientes:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{entrada['nombre']}** ({entrada['tipo']}) - Cédula: {entrada['cedula']}")
                    with col2:
                        if st.button(f"Aprobar QR", key=entrada["id"]):
                            entrada["estado"] = "APROBADO"
                            st.rerun()
            else:
                st.success("¡No hay entradas pendientes por aprobar!")
            
            st.divider()
            st.subheader("Entradas Aprobadas y Códigos QR Generados")
            aprobadas = [e for e in st.session_state["entradas"] if e["estado"] == "APROBADO"]
            
            for e in aprobadas:
                with st.expander(f"🎫 QR para {e['nombre']} - [{e['tipo']}]"):
                    # Contenido que tendrá el QR
                    contenido_qr = f"ID: {e['id']}\nNombre: {e['nombre']}\nCedula: {e['cedula']}\nTipo: {e['tipo']}\nEstado: APROBADO"
                    
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(contenido_qr)
                    qr.make(fit=True)
                    img_qr = qr.make_image(fill_color="black", back_color="white")
                    
                    buf = io.BytesIO()
                    img_qr.save(buf)
                    
                    st.image(buf, caption=f"Entrada Aprobada - ID: {e['id']}", width=250)
    elif clave != "":
        st.error("Clave incorrecta.")
