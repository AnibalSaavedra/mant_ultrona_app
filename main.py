import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

st.set_page_config(page_title="Mantenimiento Mensual ULTRONA", page_icon="🛠️", layout="centered")
st.title("🛠️ Registro de Mantenimiento Mensual - ULTRONA")

EXCEL_FILE = "registro_mant_ultrona.xlsx"

def hacer_respaldo(df):
    if not os.path.exists("respaldos"):
        os.makedirs("respaldos")
    respaldo_path = os.path.join("respaldos", f"respaldo_mant_ultrona_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    df.to_excel(respaldo_path, index=False)

if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Fecha y Hora", "Mantenimiento Realizado", "Operador"])

with st.form("form_mantenimiento"):
    fecha_hora = st.datetime_input("📅 Fecha y Hora", value=datetime.now())
    mantenimiento = st.selectbox("🔧 Mantenimiento Realizado", [
        "Remover y limpiar el deposito de basura",
        "Limpiar la plataforma de la tira y del deposito de residuos",
        "Limpieza del transportador de tira",
        "Limpieza y desinfección externa",
        "Calibración",
        "Cambio de papel",
        "Cambio de fusibles"
    ])
    operador = st.selectbox("👨‍🔧 Operador", [
        "Anibal Saavedra", "Juan Ramos", "Nycole Farias",
        "Stefanie Maureira", "Maria J.Vera", "Felipe Fernandez",
        "Paula Gutierrez", "Paola Araya", "Maria Rodriguez", "Pamela Montenegro"
    ])

    submit = st.form_submit_button("✅ Guardar Registro")

    if submit:
        nueva_fila = {
            "Fecha y Hora": fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "Mantenimiento Realizado": mantenimiento,
            "Operador": operador
        }
        df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        hacer_respaldo(df)
        st.success("✅ Registro guardado exitosamente.")

st.markdown("### 📋 Registros Anteriores")
filtro_mes = st.selectbox("📆 Filtrar por mes:", ["Todos"] + sorted(list(set(pd.to_datetime(df["Fecha y Hora"]).dt.strftime("%Y-%m").tolist()))))
if filtro_mes != "Todos":
    df_filtrado = df[pd.to_datetime(df["Fecha y Hora"]).dt.strftime("%Y-%m") == filtro_mes]
else:
    df_filtrado = df

st.dataframe(df_filtrado, use_container_width=True)

def to_excel_memory(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    label="📥 Descargar Excel",
    data=to_excel_memory(df_filtrado),
    file_name=f"mant_ultrona_{filtro_mes}.xlsx" if filtro_mes != "Todos" else "mant_ultrona_completo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)