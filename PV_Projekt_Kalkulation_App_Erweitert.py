import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf

# App title
st.set_page_config(page_title="PV-Projekt Kalkulation", layout="wide")
st.title("☀️ Qrauts AG PV-Projekt Kalkulation & Analyse by Master Marek")

# Sidebar inputs
st.sidebar.header("🔧 Eingabeparameter")

# Technische Parameter
anlage_kwp = st.sidebar.number_input("Anlagengröße (kWp)", min_value=1.0, value=100.0)
spez_ertrag = st.sidebar.number_input("Spezifischer Ertrag (kWh/kWp)", min_value=500.0, value=950.0)
eigenverbrauchsanteil = st.sidebar.slider("Eigenverbrauchsanteil (%)", min_value=0, max_value=100, value=60)
systemnutzungsgrad = st.sidebar.slider("Systemnutzungsgrad (%)", min_value=50, max_value=100, value=90)
lebensdauer = st.sidebar.slider("Lebensdauer der Anlage (Jahre)", min_value=1, max_value=40, value=25)

# Wirtschaftliche Parameter
strompreis_mieter = st.sidebar.number_input("Mieterstrompreis (ct/kWh)", min_value=10.0, value=26.0)
einspeisevergütung = st.sidebar.number_input("Einspeisevergütung (ct/kWh)", min_value=0.0, value=7.5)
inflation = st.sidebar.slider("Inflation / Preissteigerung (%)", min_value=0.0, max_value=10.0, value=2.0)

# Investitionskosten
capex = st.sidebar.number_input("Investitionskosten gesamt (€)", min_value=1000.0, value=120000.0)

# Betriebskosten
opex = st.sidebar.number_input("Jährliche Betriebskosten (€)", min_value=0.0, value=2500.0)

# Teilnehmerquote Analyse
st.sidebar.header("👥 Teilnehmerquote Analyse")
fixkosten = st.sidebar.number_input("Fixkosten (€)", min_value=0.0, value=5000.0)
variable_kosten = st.sidebar.number_input("Variable Kosten pro Teilnehmer (€)", min_value=0.0, value=50.0)
max_teilnehmer = st.sidebar.slider("Maximale Teilnehmeranzahl", min_value=1, max_value=500, value=100)

# Stromproduktion
jahresproduktion = anlage_kwp * spez_ertrag * (systemnutzungsgrad / 100)

# Einnahmenberechnung
jahreserlös = []
cashflows = []
for jahr in range(lebensdauer):
    preissteigerung = (1 + inflation / 100) ** jahr
    eigenverbrauch_kwh = jahresproduktion * (eigenverbrauchsanteil / 100)
    einspeisung_kwh = jahresproduktion - eigenverbrauch_kwh
    erlös = eigenverbrauch_kwh * strompreis_mieter / 100 * preissteigerung + einspeisung_kwh * einspeisevergütung / 100 * preissteigerung
    kosten = opex * preissteigerung
    cashflow = erlös - kosten
    jahreserlös.append(erlös)
    cashflows.append(cashflow)

# Kumulierte Cashflows
kumuliert = np.cumsum(cashflows)
break_even_jahr = next((i for i, x in enumerate(kumuliert) if x >= capex), None)

# Tabs
tab1, tab2 = st.tabs(["📈 Cashflow & Break-even", "👥 Teilnehmerquote & Strompreis"])

with tab1:
    st.subheader("📊 Cashflow Verlauf")
    fig, ax = plt.subplots()
    ax.plot(range(1, lebensdauer + 1), cashflows, label="Jährlicher Cashflow")
    ax.plot(range(1, lebensdauer + 1), kumuliert, label="Kumulierte Cashflows")
    if break_even_jahr is not None:
        ax.axvline(break_even_jahr + 1, color='red', linestyle='--', label=f"Break-even: Jahr {break_even_jahr + 1}")
    ax.set_xlabel("Jahr")
    ax.set_ylabel("€")
    ax.legend()
    st.pyplot(fig)

    st.markdown(f"**Amortisationszeitpunkt:** Jahr {break_even_jahr + 1}" if break_even_jahr is not None else "❌ Kein Break-even innerhalb der Lebensdauer")

with tab2:
    st.subheader("👥 Strompreis pro kWh in Abhängigkeit von Teilnehmerquote")
    teilnehmer_range = np.arange(1, max_teilnehmer + 1)
    strompreise = (fixkosten + variable_kosten * teilnehmer_range) / (jahresproduktion * (eigenverbrauchsanteil / 100))

    df_preise = pd.DataFrame({
        "Teilnehmeranzahl": teilnehmer_range,
        "Strompreis (€/kWh)": strompreise
    })

    fig2, ax2 = plt.subplots()
    ax2.plot(df_preise["Teilnehmeranzahl"], df_preise["Strompreis (€/kWh)"], color='green')
    ax2.set_xlabel("Teilnehmeranzahl")
    ax2.set_ylabel("Strompreis (€/kWh)")
    ax2.set_title("Strompreis vs. Teilnehmerquote")
    st.pyplot(fig2)

    st.dataframe(df_preise.head(20))

st.markdown("---")
st.markdown("📌 Hinweis von developer Marek Wulff: Diese App dient der vereinfachten Modellierung eines PV-Mieterstromprojekts. Für detaillierte Wirtschaftlichkeitsanalysen empfehlen wir eine professionelle Beratung.")
