import streamlit as st
import pandas as pd
import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Control de Gastos", page_icon="💸")

st.title("💸 Mi Gestor de Gastos")
st.markdown("---")

# Archivo donde se guardarán los datos
DATA_FILE = "mis_gastos.csv"

# Definición de categorías según lo conversado
categorias = {
    "Fijos": [
        "Luz", "Agua", "Gas", "Internet", "Streaming", 
        "Pastilla de mamá", "Pensión mamá (Adelantada)", 
        "Préstamo banco", "Celular", "Mantenimiento"
    ],
    "Variables": [
        "Comida", "Pasajes", "Gustos", 
        "Artículos de limpieza", "Pago Tarjeta de Crédito"
    ]
}

# --- FORMULARIO ---
with st.form(key="formulario_gastos", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        fecha = st.date_input("Fecha", datetime.date.today())
        tipo = st.selectbox("Tipo de Gasto", ["Fijos", "Variables"])
        
    with col2:
        monto = st.number_input("Monto ($)", min_value=0.0, step=0.50, format="%.2f")
        # El submenú cambia según si eliges Fijo o Variable
        subcategoria = st.selectbox("Subcategoría", categorias[tipo])

    descripcion = st.text_input("Descripción / Nota adicional")
    
    boton_guardar = st.form_submit_button(label="Registrar Gasto 💾")

# --- LÓGICA DE GUARDADO ---
if boton_guardar:
    nuevo_dato = {
        "Fecha": fecha,
        "Tipo": tipo,
        "Subcategoría": subcategoria,
        "Monto": monto,
        "Descripción": descripcion
    }
    
    df_nuevo = pd.DataFrame([nuevo_dato])

    # Si el archivo no existe, se crea con encabezados. Si existe, se añade la fila.
    if not os.path.isfile(DATA_FILE):
        df_nuevo.to_csv(DATA_FILE, index=False)
    else:
        df_nuevo.to_csv(DATA_FILE, mode='a', index=False, header=False)
        
    st.success(f"¡Registrado! {subcategoria}: ${monto}")

# --- SECCIÓN DE DASHBOARD (Básico) ---
st.markdown("---")
if st.checkbox("📊 Mostrar Resumen Rápido"):
    if os.path.isfile(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        
        st.subheader("Gastos Totales por Tipo")
        resumen = df.groupby("Tipo")["Monto"].sum()
        st.bar_chart(resumen)
        
        st.subheader("Últimos Registros")
        st.dataframe(df.tail(5))
    else:
        st.info("Aún no hay datos registrados.")
