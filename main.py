import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

st.set_page_config(page_title="Registro Mantenimiento ULTRONA", page_icon="🛠️", layout="centered")
st.title("🛠️ Registro de Mantenimiento Mensual - ULTRONA")

EXCEL_FILE = "registro_ultrona.xlsx"
RESPALDO_DIR = "respaldos_ultrona"

# Cargar o crear DataFrame
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=[
        "Fecha y Hora", "Mantenimiento Realizado", "Operador"
    ])

# Función de respaldo automático
def hacer_respaldo():
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    respaldo_path = os.path.join(RESPALDO_DIR, f"respaldo_ultrona_{fecha_hora}.xlsx")
    df.to_excel(respaldo_path, index=False)

hacer_respaldo()

# Formulario de ingreso
with st.form("form_mantencion"):
    fecha_hora = st.text_input("📅 Fecha y Hora", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mantencion = st.selectbox("🔧 Mantenimiento Realizado", [
        "Remover y limpiar el deposito de basura",
        "Limpiar la plataforma de la tira y del deposito de residuos",
        "Limpieza del transportador de tira",
        "Limpieza y desinfeccion externa",
        "Calibracion",
        "Cambio de papel",
        "Cambio de fusibles"
    ])
    operador = st.selectbox("👨‍🔧 Operador", [
        "Anibal Saavedra", "Juan Ramos", "Nycole Farias", "Stefanie Maureira",
        "Maria J.Vera", "Felipe Fernandez", "Paula Gutierrez", "Paola Araya",
        "Maria Rodriguez", "Pamela Montenegro"
    ])
    enviar = st.form_submit_button("✅ Guardar Registro")

    if enviar:
        nueva_fila = {
            "Fecha y Hora": fecha_hora,
            "Mantenimiento Realizado": mantencion,
            "Operador": operador
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        hacer_respaldo()
        st.success("Registro guardado correctamente.")

# Filtro por mes
st.markdown("### 📆 Filtrar por Mes")
meses = df["Fecha y Hora"].apply(lambda x: str(x)[:7]).unique()
mes_seleccionado = st.selectbox("Selecciona un mes", opciones := sorted(meses, reverse=True))
df_filtrado_mes = df[df["Fecha y Hora"].str.startswith(mes_seleccionado)]
st.dataframe(df_filtrado_mes)

# Búsqueda por texto
st.markdown("### 🔍 Buscar Registros")
busqueda = st.text_input("Buscar por palabra clave (mantenimiento u operador):")
if busqueda:
    df_busqueda = df[df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    st.dataframe(df_busqueda)

# Descargar por fecha
st.markdown("### 📥 Descargar Registros por Fecha")
fecha_descarga = st.date_input("Selecciona una fecha para descargar:")
fecha_str = fecha_descarga.strftime("%Y-%m-%d")
df_fecha = df[df["Fecha y Hora"].str.startswith(fecha_str)]
if not df_fecha.empty:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_fecha.to_excel(writer, index=False)
    st.download_button(
        label=f"📤 Descargar registros del {fecha_str}",
        data=output.getvalue(),
        file_name=f"registros_ultrona_{fecha_str}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No hay registros para esta fecha.")