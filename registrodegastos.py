import streamlit as st
import pandas as pd
import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Mi Control Financiero", page_icon="💰", layout="wide")

DATA_FILE = "mis_gastos.csv"

# Definición de categorías
categorias = {
    "Fijos": ["Luz", "Agua", "Gas", "Internet", "Streaming", "Pastilla de mamá", 
              "Pensión mamá (Adelantada)", "Préstamo banco", "Celular", "Mantenimiento"],
    "Variables": ["Comida", "Pasajes", "Gustos", "Artículos de limpieza", "Pago Tarjeta de Crédito"]
}

# --- FUNCIONES AUXILIARES ---
def cargar_datos():
    if os.path.isfile(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Fecha", "Tipo", "Subcategoría", "Monto", "Método", "Estado", "Descripción"])

# --- DASHBOARD DE TOTALES (En la parte superior) ---
df_actual = cargar_datos()
total_gastado = df_actual["Monto"].sum() if not df_actual.empty else 0.0

st.title("💰 Mi Gestor de Gastos Detallado")
col_m1, col_m2 = st.columns(2)
col_m1.metric("Total Gastado Histórico", f"${total_gastado:,.2f}")
col_m2.metric("Registros Totales", len(df_actual))

st.markdown("---")

# --- FORMULARIO CON MÁS DETALLE ---
st.subheader("📝 Registrar Nuevo Movimiento")
with st.form(key="formulario_detallado", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        fecha = st.date_input("Fecha", datetime.date.today())
        tipo = st.selectbox("Tipo de Gasto", ["Fijos", "Variables"])
        subcategoria = st.selectbox("Subcategoría", categorias[tipo])
        
    with c2:
        monto = st.number_input("Monto ($)", min_value=0.0, step=0.10, format="%.2f")
        metodo = st.selectbox("Método de Pago", ["Efectivo", "Débito", "Crédito", "Transferencia"])
        
    with c3:
        estado = st.selectbox("Estado del Gasto", ["Pagado", "Pendiente", "Pre-pagado (Adelanto)"])
        descripcion = st.text_area("Notas / Detalles (Ej: Marca de jabón, Mes de luz)")

    submit = st.form_submit_button("Guardar Registro 💾")

if submit:
    nuevo_registro = pd.DataFrame([{
        "Fecha": fecha, "Tipo": tipo, "Subcategoría": subcategoria,
        "Monto": monto, "Método": metodo, "Estado": estado, "Descripción": descripcion
    }])
    
    if not os.path.isfile(DATA_FILE):
        nuevo_registro.to_csv(DATA_FILE, index=False)
    else:
        nuevo_registro.to_csv(DATA_FILE, mode='a', index=False, header=False)
    
    st.success(f"✅ Registrado: {subcategoria} por ${monto}")
    st.rerun() # Recarga la página para actualizar el total arriba

# --- SECCIÓN DE ANÁLISIS ---
st.markdown("---")
st.subheader("📊 Análisis de Gastos")

tab1, tab2 = st.tabs(["Detalle por Categoría", "Historial Completo"])

with tab1:
    if not df_actual.empty:
        # Agrupación por subcategoría para ver el gasto acumulado
        resumen_sub = df_actual.groupby("Subcategoría")["Monto"].sum().sort_values(ascending=False)
        st.bar_chart(resumen_sub)
        st.write(resumen_sub)
    else:
        st.info("No hay datos para mostrar gráficos.")

with tab2:
    st.dataframe(df_actual.sort_values(by="Fecha", ascending=False), use_container_width=True)
