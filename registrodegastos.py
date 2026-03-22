import streamlit as st
import pandas as pd
import datetime
import os

# CONFIGURACIÓN
st.set_page_config(page_title="Control de Gastos Pro", page_icon="📊", layout="wide")
DATA_FILE = "mis_gastos.csv"

categorias = {
    "Fijos": ["Luz", "Agua", "Gas", "Internet", "Streaming", "Pastilla de mamá", 
              "Pensión mamá (Adelantada)", "Préstamo banco", "Celular", "Mantenimiento", "Comida", "Pasajes", "Gustos", "Artículos de limpieza", "Pago Tarjeta de Créd"],
    "Variables": ["Comida", "Pasajes", "Gustos", "Artículos de limpieza", "Pago Tarjeta de Crédito"]
}

def cargar_datos():
    if os.path.isfile(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
        return df
    return pd.DataFrame(columns=["Fecha", "Tipo", "Subcategoría", "Monto", "Método", "Estado", "Descripción"])

df_actual = cargar_datos()

# --- TÍTULO Y MÉTRICAS ---
st.title("📊 Dashboard & Gestión de Gastos")
total_gastado = df_actual["Monto"].sum() if not df_actual.empty else 0.0
st.metric("Gasto Total Acumulado", f"${total_gastado:,.2f}")

# --- PESTAÑAS PARA ORGANIZAR ---
tab_reg, tab_dash, tab_edit = st.tabs(["📝 Registrar", "📈 Dashboard", "✏️ Editar/Borrar"])

# --- TAB 1: REGISTRO ---
with tab_reg:
    with st.form(key="form_registro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            fecha = st.date_input("Fecha", datetime.date.today())
            tipo = st.selectbox("Tipo", ["Fijos", "Variables"])
            sub = st.selectbox("Subcategoría", categorias[tipo])
        with c2:
            monto = st.number_input("Monto", min_value=0.0, format="%.2f")
            metodo = st.selectbox("Método", ["Efectivo", "Débito", "Crédito", "Transferencia"])
            estado = st.selectbox("Estado", ["Pagado", "Pendiente", "Pre-pagado"])
        
        desc = st.text_input("Descripción")
        if st.form_submit_button("Guardar"):
            nuevo = pd.DataFrame([{"Fecha": fecha, "Tipo": tipo, "Subcategoría": sub, "Monto": monto, "Método": metodo, "Estado": estado, "Descripción": desc}])
            nuevo.to_csv(DATA_FILE, mode='a', index=False, header=not os.path.isfile(DATA_FILE))
            st.success("Registrado correctamente")
            st.rerun()

# --- TAB 2: DASHBOARD ---
with tab_dash:
    if not df_actual.empty:
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.subheader("Distribución por Tipo")
            # Gráfico de pastel
            fig_tipo = df_actual.groupby("Tipo")["Monto"].sum()
            st.bar_chart(fig_tipo)
            
        with col_d2:
            st.subheader("Gastos por Subcategoría")
            fig_sub = df_actual.groupby("Subcategoría")["Monto"].sum().sort_values()
            st.bar_chart(fig_sub)
            
        st.subheader("Historial Reciente")
        st.dataframe(df_actual.sort_values(by="Fecha", ascending=False), use_container_width=True)
    else:
        st.info("Agrega datos para ver el dashboard.")

# --- TAB 3: EDITAR ---
with tab_edit:
    if not df_actual.empty:
        st.subheader("Modificar un registro")
        # Seleccionar por índice para editar
        df_edit = df_actual.copy()
        df_edit['ID'] = df_edit.index
        opciones = [f"ID {i}: {row['Fecha']} - {row['Subcategoría']} (${row['Monto']})" for i, row in df_edit.iterrows()]
        seleccion = st.selectbox("Selecciona el registro a editar", opciones)
        
        id_selecc = int(seleccion.split(":")[0].replace("ID ", ""))
        fila = df_actual.iloc[id_selecc]
        
        with st.form("form_edit"):
            c1, c2 = st.columns(2)
            new_fecha = c1.date_input("Nueva Fecha", fila['Fecha'])
            new_sub = c1.selectbox("Nueva Subcategoría", categorias["Fijos"] + categorias["Variables"], index=0)
            new_monto = c2.number_input("Nuevo Monto", value=float(fila['Monto']))
            new_desc = c2.text_input("Nueva Descripción", value=fila['Descripción'])
            
            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.form_submit_button("Actualizar Registro"):
                df_actual.at[id_selecc, 'Fecha'] = new_fecha
                df_actual.at[id_selecc, 'Subcategoría'] = new_sub
                df_actual.at[id_selecc, 'Monto'] = new_monto
                df_actual.at[id_selecc, 'Descripción'] = new_desc
                df_actual.to_csv(DATA_FILE, index=False)
                st.success("Registro actualizado")
                st.rerun()
                
            if col_btn2.form_submit_button("❌ Eliminar este registro"):
                df_actual = df_actual.drop(id_selecc)
                df_actual.to_csv(DATA_FILE, index=False)
                st.warning("Registro eliminado")
                st.rerun()
    else:
        st.info("No hay datos para editar.")
