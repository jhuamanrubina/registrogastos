import streamlit as st
import pandas as pd
import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA ANCHA (Para que el cuadro se vea completo)
st.set_page_config(page_title="Control de Gastos", page_icon="💰", layout="wide")

DATA_FILE = "mis_gastos.csv"

# Diccionario de categorías
categorias = {
    "Fijos": ["Luz", "Agua", "Gas", "Internet", "Streaming", "Pastilla de mamá", 
              "Pensión mamá (Adelantada)", "Préstamo banco", "Celular", "Mantenimiento"],
    "Variables": ["Comida", "Pasajes", "Gustos", "Artículos de limpieza", "Pago Tarjeta de Crédito"]
}

def cargar_datos():
    if os.path.isfile(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Fecha", "Tipo", "Subcategoría", "Monto", "Método", "Estado", "Descripción"])

df_actual = cargar_datos()

st.title("💰 Mi Gestor de Gastos")

# Métricas rápidas
total_gastado = df_actual["Monto"].sum() if not df_actual.empty else 0.0
st.metric("Gasto Total Acumulado", f"${total_gastado:,.2f}")

st.markdown("---")

# --- FORMULARIO CORREGIDO ---
st.subheader("📝 Nuevo Registro")
with st.form(key="form_gastos", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fecha = st.date_input("Fecha", datetime.date.today())
        # Al cambiar este, el siguiente selectbox se actualizará al enviar o recargar
        tipo_sel = st.selectbox("Tipo de Gasto", ["Fijos", "Variables"], key="tipo_gasto")
        
    with col2:
        # Aquí filtramos las subcategorías según la elección anterior
        sub_sel = st.selectbox("Subcategoría", categorias[tipo_sel])
        monto = st.number_input("Monto ($)", min_value=0.0, format="%.2f")
        
    with col3:
        metodo = st.selectbox("Método", ["Efectivo", "Débito", "Crédito", "Transferencia"])
        estado = st.selectbox("Estado", ["Pagado", "Pendiente", "Pre-pagado"])

    descripcion = st.text_input("Descripción corta")
    enviar = st.form_submit_button("Guardar Gasto 💾")

if enviar:
    nuevo = pd.DataFrame([{
        "Fecha": fecha, "Tipo": tipo_sel, "Subcategoría": sub_sel,
        "Monto": monto, "Método": metodo, "Estado": estado, "Descripción": descripcion
    }])
    nuevo.to_csv(DATA_FILE, mode='a', index=False, header=not os.path.isfile(DATA_FILE))
    st.success("¡Guardado correctamente!")
    st.rerun()

st.markdown("---")

# --- CUADRO COMPLETO DE GASTOS ---
st.subheader("📊 Historial Completo de Gastos")

if not df_actual.empty:
    # Mostramos el dataframe usando TODO el ancho de la pantalla
    # Ordenado por fecha para que veas lo más reciente arriba
    st.dataframe(
        df_actual.sort_values(by="Fecha", ascending=False), 
        use_container_width=True, # ESTO hace que el cuadro sea completo
        hide_index=True
    )
else:
    st.info("No hay registros todavía.")

# --- BOTÓN PARA BORRAR TODO ---
with st.expander("⚙️ Opciones de sistema"):
    if st.button("🗑️ Borrar base de datos"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.rerun()
