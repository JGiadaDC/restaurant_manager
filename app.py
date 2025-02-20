import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

# Nome del file Excel per salvare i dati
DB_FILE = "database_fornitori.xlsx"

# Inizializza i dati se non esistono
if "spese_data" not in st.session_state:
    st.session_state.spese_data = []
if "incassi_data" not in st.session_state:
    st.session_state.incassi_data = []

# Funzione per salvare i dati su Excel
def salva_su_excel():
    df_spese = pd.DataFrame(st.session_state.spese_data)
    df_incassi = pd.DataFrame(st.session_state.incassi_data)

    with pd.ExcelWriter(DB_FILE, engine="openpyxl", mode="w") as writer:
        df_spese.to_excel(writer, sheet_name="Spese", index=False)
        df_incassi.to_excel(writer, sheet_name="Incassi", index=False)

# Funzione per caricare i dati da Excel se il file esiste
def carica_da_excel():
    if os.path.exists(DB_FILE):
        with pd.ExcelFile(DB_FILE) as xls:
            st.session_state.spese_data = pd.read_excel(xls, sheet_name="Spese").to_dict("records")
            st.session_state.incassi_data = pd.read_excel(xls, sheet_name="Incassi").to_dict("records")

# Carichiamo i dati all'avvio
carica_da_excel()


# Funzione per aggiungere una spesa
def aggiungi_spesa():
    st.subheader("Inserisci Spesa")
    data = st.date_input("Seleziona la data")
    categoria = st.selectbox("Seleziona Categoria", ["FOOD", "BEVERAGE", "ALTRO"])
    fornitore = st.selectbox("Seleziona Fornitore", ["ANIOFE", "GASEOSA", "METRO", "MERCADONA", "PANE", "LATTE"])
    importo = st.number_input("Importo (€)", min_value=0.0, step=0.01)

    if st.button("Aggiungi Spesa"):
        nuova_spesa = {"Data": data, "Categoria": categoria, "Fornitore": fornitore, "Importo": importo}
        st.session_state.spese_data.append(nuova_spesa)
        salva_su_excel()
        st.success("Spesa aggiunta con successo!")

# Funzione per aggiungere un incasso
def aggiungi_incasso():
    st.subheader("Inserisci Incasso")
    data = st.date_input("Seleziona la data")
    contanti = st.number_input("Contanti (€)", min_value=0.0, step=0.01)
    pos = st.number_input("POS (€)", min_value=0.0, step=0.01)

    if st.button("Aggiungi Incasso"):
        nuovo_incasso = {"Data": data, "Contanti": contanti, "POS": pos, "Totale": contanti + pos}
        st.session_state.incassi_data.append(nuovo_incasso)
        salva_su_excel()
        st.success("Incasso aggiunto con successo!")


# Funzione per visualizzare dati con filtro per intervallo di tempo e fornitore
# Funzione per visualizzare dati con filtro per intervallo di tempo e fornitore
def visualizza_dati():
    st.subheader("Visualizza Dati: Spese e Incassi")

    # Selezione intervallo di date
    date_range = st.date_input("Seleziona un intervallo di date", [], help="Seleziona l'intervallo di tempo per visualizzare i dati.")

    # Selezione fornitore
    selected_fornitore = st.selectbox("Seleziona un fornitore", ["Tutti"] + list(set(d["Fornitore"] for d in st.session_state.spese_data)))

    # === 📌 VISUALIZZAZIONE SPESE ===
    if st.session_state.spese_data:
        df_spese = pd.DataFrame(st.session_state.spese_data)
        df_spese["Data"] = pd.to_datetime(df_spese["Data"]).dt.date  # Convertiamo in formato data

        # Filtriamo per intervallo di date
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            df_spese = df_spese[(df_spese["Data"] >= start_date) & (df_spese["Data"] <= end_date)]

        # Filtriamo per fornitore
        if selected_fornitore != "Tutti":
            df_spese = df_spese[df_spese["Fornitore"] == selected_fornitore]

        # Mostriamo i dati filtrati
        if not df_spese.empty:
            for i, row in df_spese.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                col1.write(row["Data"])
                col2.write(row["Categoria"])
                col3.write(row["Fornitore"])
                col4.write(f"{row['Importo']:.2f} €")

                if col5.button("❌", key=f"del_spesa_{i}"):
                    st.session_state.spese_data.pop(i)
                    salva_su_excel()
                    st.rerun()  # Ricarica la pagina per aggiornare la visualizzazione

            totale_spese = df_spese["Importo"].sum()
            st.write(f"### Totale spese per {selected_fornitore}: {totale_spese:.2f} €")
        else:
            st.write("Nessuna spesa trovata per il periodo selezionato.")

    else:
        st.write("Nessuna spesa disponibile.")
        

    # === 📌 VISUALIZZAZIONE INCASSI ===
    if st.session_state.incassi_data:
        df_incassi = pd.DataFrame(st.session_state.incassi_data)
        df_incassi["Data"] = pd.to_datetime(df_incassi["Data"]).dt.date  # Convertiamo in formato data

        # Filtriamo per intervallo di date
        if date_range and len(date_range) == 2:
            start_date, end_date = date_range
            df_incassi = df_incassi[(df_incassi["Data"] >= start_date) & (df_incassi["Data"] <= end_date)]

        # Calcoliamo il totale incassi per giorno
        df_incassi["Totale"] = df_incassi["Contanti"] + df_incassi["POS"]

        if not df_incassi.empty:
            for i, row in df_incassi.iterrows():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                col1.write(row["Data"])
                col2.write(f"Contanti: {row['Contanti']:.2f} €")
                col3.write(f"POS: {row['POS']:.2f} €")

                if col4.button("❌", key=f"del_incasso_{i}"):
                    st.session_state.incassi_data.pop(i)
                    salva_su_excel()
                    st.rerun()
        else:
            st.write("Nessun incasso trovato.")

    else:
        st.write("Nessun incasso disponibile.")
        

# Funzione per visualizzare il grafico del Food Cost e del Guadagno

def visualizza_grafici():
    st.subheader("📊 Analisi: Food Cost & Guadagno")

    if st.session_state.spese_data and st.session_state.incassi_data:
        df_spese = pd.DataFrame(st.session_state.spese_data)
        df_incassi = pd.DataFrame(st.session_state.incassi_data)

        df_spese["Data"] = pd.to_datetime(df_spese["Data"]).dt.date
        df_incassi["Data"] = pd.to_datetime(df_incassi["Data"]).dt.date

        # === 📌 GRAFICO FOOD COST ===
        st.subheader("Food Cost")

        if not df_spese.empty:
            categorie_spese = df_spese.groupby("Categoria")["Importo"].sum().reset_index()

            fig_pie = px.pie(
                categorie_spese, 
                names="Categoria", 
                values="Importo",
                title="Distribuzione delle Spese per Categoria",
                color="Categoria",
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            st.plotly_chart(fig_pie)

        # === 📌 GRAFICO GUADAGNO NEL TEMPO ===
        st.subheader("Andamento del Guadagno")

        spese_per_data = df_spese.groupby("Data")["Importo"].sum().reset_index()
        incassi_per_data = df_incassi.groupby("Data")["Totale"].sum().reset_index()

        df_guadagno = pd.merge(incassi_per_data, spese_per_data, on="Data", how="outer").fillna(0)
        df_guadagno["Guadagno"] = df_guadagno["Totale"] - df_guadagno["Importo"]

        fig_line = px.line(df_guadagno, x="Data", y="Guadagno", markers=True, title="Guadagno giornaliero",
                           labels={"Guadagno": "€"},
                           color_discrete_sequence=["green"])
        fig_line.update_layout(xaxis_title="Data", yaxis_title="Guadagno (€)", xaxis_tickangle=-45)

        st.plotly_chart(fig_line)

    else:
        st.write("Dati insufficienti per generare i grafici.")

# Funzione principale
def main():
    st.title("Gestione Spese e Incassi 📊")

    pagina = st.sidebar.selectbox("Seleziona una sezione", ["Inserisci Spesa", "Inserisci Incasso", "Visualizza Dati", "Analisi & Grafici"])

    if pagina == "Inserisci Spesa":
        aggiungi_spesa()
    elif pagina == "Inserisci Incasso":
        aggiungi_incasso()
    elif pagina == "Visualizza Dati":
        visualizza_dati()
    elif pagina == "Analisi & Grafici":
        visualizza_grafici()

if __name__ == "__main__":
    main()
