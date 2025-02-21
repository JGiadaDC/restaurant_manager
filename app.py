import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

# Excel file
DB_FILE = "database_fornitori.xlsx"

# Initialize session state if it does not exist
if "spese_data" not in st.session_state:
    st.session_state.spese_data = []
if "incassi_data" not in st.session_state:
    st.session_state.incassi_data = []

# Function to load data from Excel if the file exists
def carica_da_excel():
    if os.path.exists(DB_FILE):
        with pd.ExcelFile(DB_FILE, engine="openpyxl") as xls:
            st.session_state.spese_data = pd.read_excel(xls, sheet_name="Spese").to_dict("records")
            st.session_state.incassi_data = pd.read_excel(xls, sheet_name="Incassi").to_dict("records")

# Load data on startup
carica_da_excel()

# Function to save data to Excel
def salva_su_excel():
    df_spese = pd.DataFrame(st.session_state.spese_data)
    df_incassi = pd.DataFrame(st.session_state.incassi_data)

    with pd.ExcelWriter(DB_FILE, engine="openpyxl", mode="w") as writer:
        df_spese.to_excel(writer, sheet_name="Spese", index=False)
        df_incassi.to_excel(writer, sheet_name="Incassi", index=False)



# Function to add an expense
def aggiungi_spesa():
    st.subheader("📌Ingresar Gasto")
    data = st.date_input("Seleccionar fecha")
    categoria = st.selectbox("Seleccionar Categoría", ["FOOD", "BEVERAGE", "OTROS"])
    fornitore = st.selectbox("Seleccionar Proveedor", ["ANIOFE", "IBIFOOD", "BUENAS MIGAS Y MAS", "BE DRINKS", "PROMOCIONES COMERCIALES", "ENOTECUM", "PASCUCCI", "COCA COLA", "IBIPELMAR", "FRUTAS MARCH", "ALGAR"])
    importo = st.number_input("Importe (€)", min_value=0.0, step=0.01)

    if st.button("Agregar Gasto"):
        nuova_spesa = {"Fecha": data, "Categoria": categoria, "Proveedor": fornitore, "Importe": importo}
        st.session_state.spese_data.append(nuova_spesa)
        salva_su_excel()
        st.success("¡Gasto agregado exitosamente!")

# Function to add an income
def aggiungi_incasso():
    st.subheader("📌 Ingresar Ingreso")
    data = st.date_input("Seleccionar fecha")
    contanti = st.number_input("Efectivo (€)", min_value=0.0, step=0.01)
    pos = st.number_input("POS (€)", min_value=0.0, step=0.01)

    if st.button("Agregar Ingreso"):
        nuovo_incasso = {"Fecha": data, "Efectivo": contanti, "POS": pos, "Total": contanti + pos}
        st.session_state.incassi_data.append(nuovo_incasso)
        salva_su_excel()
        st.success("¡Ingreso agregado exitosamente!")



# Function to view data with filters
def visualizza_dati():
    st.subheader("📊 Ver Datos: Gastos e Ingresos")

    # Select a data range
    date_range = st.date_input("Seleccionar intervalo de fechas", [], help="Selecciona el período para ver los datos.")

    # Select provider
    selected_fornitore = st.selectbox("Seleccionar proveedor", ["Todos"] + list(set(d["Proveedor"] for d in st.session_state.spese_data)))

    # === 📌 Display expenses ===
    if st.session_state.spese_data:
        df_spese = pd.DataFrame(st.session_state.spese_data)
        df_spese["Fecha"] = pd.to_datetime(df_spese["Fecha"]).dt.date # convert to data

        # Filter
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            df_spese = df_spese[(df_spese["Fecha"] >= start_date) & (df_spese["Fecha"] <= end_date)]

        # Filter
        if selected_fornitore != "Todos":
            df_spese = df_spese[df_spese["Proveedor"] == selected_fornitore]

        # Show filtered data
        if not df_spese.empty:
            for i, row in df_spese.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                col1.write(row["Fecha"])
                col2.write(row["Categoria"])
                col3.write(row["Proveedor"])
                col4.write(f"{row['Importe']:.2f} €")

                if col5.button("❌", key=f"del_spesa_{i}"):
                    st.session_state.spese_data.pop(i)
                    salva_su_excel()
                    st.rerun()  # Rerun to update

            totale_spese = df_spese["Importe"].sum()
            st.write(f"### Total gastos para {selected_fornitore}: {totale_spese:.2f} €")
        else:
            st.write("Ningun gasto encontrado en el periodo seleccionado.")

    else:
        st.write("Ningun gasto disponible.")
        

    # === 📌 Display incomes ===
    if st.session_state.incassi_data:
        df_incassi = pd.DataFrame(st.session_state.incassi_data)
        df_incassi["Fecha"] = pd.to_datetime(df_incassi["Fecha"]).dt.date  # Convertiamo in formato data

        # Filter date
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            df_incassi = df_incassi[(df_incassi["Fecha"] >= start_date) & (df_incassi["Fecha"] <= end_date)]

        # Total of the day
        df_incassi["Total"] = df_incassi["Efectivo"] + df_incassi["POS"]

        if not df_incassi.empty:
            for i, row in df_incassi.iterrows():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                col1.write(row["Fecha"])
                col2.write(f"Efectivo: {row['Efectivo']:.2f} €")
                col3.write(f"POS: {row['POS']:.2f} €")

                if col4.button("❌", key=f"del_incasso_{i}"):
                    st.session_state.incassi_data.pop(i)
                    salva_su_excel()
                    st.rerun()

                    # Calcoliamo e mostriamo il totale degli incassi
            totale_incassi = df_incassi["Total"].sum()
            st.write(f"**Total Ingresos: € {totale_incassi:.2f}**")
        else:
            st.write("Ningun ingreso encontrado en el periodo seleccionado.")

    else:
        st.write("Ningun ingreso disponible.")
        

# Function to display charts

def visualizza_grafici():
    st.subheader("📊 Análisis: Food Cost & Ganancia")

    if st.session_state.spese_data and st.session_state.incassi_data:
        df_spese = pd.DataFrame(st.session_state.spese_data)
        df_incassi = pd.DataFrame(st.session_state.incassi_data)

        df_spese["Fecha"] = pd.to_datetime(df_spese["Fecha"]).dt.date
        df_incassi["Fecha"] = pd.to_datetime(df_incassi["Fecha"]).dt.date

        # === 📌 FOOD COST chart ===
        st.subheader("Food Cost")

        if not df_spese.empty:
            categorie_spese = df_spese.groupby("Categoria")["Importe"].sum().reset_index()

            fig_pie = px.pie(
                categorie_spese, 
                names="Categoria", 
                values="Importe",
                title="Distribución de Gastos por Categoría",
                color="Categoria",
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            st.plotly_chart(fig_pie)

        # === 📌 Incomes Chart ===
        st.subheader("Ganancia")

        spese_per_data = df_spese.groupby("Fecha")["Importe"].sum().reset_index()
        incassi_per_data = df_incassi.groupby("Fecha")["Total"].sum().reset_index()

        df_guadagno = pd.merge(incassi_per_data, spese_per_data, on="Fecha", how="outer").fillna(0)
        df_guadagno["Ganancia"] = df_guadagno["Total"] - df_guadagno["Importe"]

        fig_line = px.line(df_guadagno, x="Fecha", y="Ganancia", markers=True, title="Ganancia diaria",
                           labels={"Ganancia": "€"},
                           color_discrete_sequence=["green"])
        fig_line.update_layout(xaxis_title="Fecha", yaxis_title="Ganancia (€)", xaxis_tickangle=-45, xaxis=dict(tickformat="%Y/%m/%d"))

        st.plotly_chart(fig_line)

    else:
        st.write("Datos insuficientes para generar graficos.")

# Main Function
def main():
    st.title("Gestión de Gastos e Ingresos 📊")

    pagina = st.sidebar.selectbox("Seleccionar sección", ["Ingresar Gasto", "Ingresar Ingreso", "Ver Datos", "Análisis & Gráficos"])

    if pagina == "Ingresar Gasto":
        aggiungi_spesa()
    elif pagina == "Ingresar Ingreso":
        aggiungi_incasso()
    elif pagina == "Ver Datos":
        visualizza_dati()
    elif pagina == "Análisis & Gráficos":
        visualizza_grafici()

if __name__ == "__main__":
    main()