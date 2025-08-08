import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy_financial as npf

st.set_page_config(page_title="PV-Projekt Kalkulation", layout="wide")

# Eingabemaske
st.sidebar.header("🔧 Eingabeparameter")

# Technische Parameter
size_kwp = st.sidebar.number_input("Anlagengröße (kWp)", value=100.0)
yield_kwh_per_kwp = st.sidebar.number_input("Spezifischer Ertrag (kWh/kWp)", value=950.0)
self_consumption_pct = st.sidebar.slider("Eigenverbrauchsanteil (%)", 0, 100, 60)
lifetime_years = st.sidebar.slider("Lebensdauer der Anlage (Jahre)", 10, 30, 20)
inflation_rate = st.sidebar.slider("Inflation / Preissteigerung (%)", 0.0, 10.0, 2.0)

# Wirtschaftliche Parameter
investment_total = st.sidebar.number_input("Investitionskosten gesamt (€)", value=120000.0)
opex_per_year = st.sidebar.number_input("Jährliche Betriebskosten (OPEX) (€)", value=2500.0)
strompreis_mieter = st.sidebar.number_input("Mieterstrompreis (ct/kWh)", value=26.0) / 100
einspeisevergütung = st.sidebar.number_input("Einspeisevergütung (ct/kWh)", value=7.0) / 100

# Teilnehmerquote-Analyse
st.sidebar.header("👥 Teilnehmerquote-Analyse")
min_teilnehmer = st.sidebar.slider("Min. Teilnehmerquote (%)", 10, 100, 30)
max_teilnehmer = st.sidebar.slider("Max. Teilnehmerquote (%)", 10, 100, 100)
fixkosten = st.sidebar.number_input("Fixkosten (€)", value=5000.0)
variable_kosten_pro_kwh = st.sidebar.number_input("Variable Kosten (ct/kWh)", value=10.0) / 100

# Berechnungen
years = np.arange(1, lifetime_years + 1)
stromertrag = size_kwp * yield_kwh_per_kwp
eigenverbrauch_kwh = stromertrag * (self_consumption_pct / 100)
einspeisung_kwh = stromertrag - eigenverbrauch_kwh

cashflows = []
for year in years:
    preissteigerung = (1 + inflation_rate / 100) ** (year - 1)
    erlöse = eigenverbrauch_kwh * strompreis_mieter * preissteigerung + einspeisung_kwh * einspeisevergütung
    kosten = opex_per_year * preissteigerung
    cashflow = erlöse - kosten
    cashflows.append(cashflow)

kumulierte_cf = np.cumsum(cashflows)
break_even_index = next((i for i, x in enumerate(kumulierte_cf) if x > investment_total), None)

# Dashboard
st.title("📊 PV-Projekt Kalkulation – Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Jährlicher Stromertrag (kWh)", f"{stromertrag:,.0f}")
col2.metric("Amortisationsjahr", f"{break_even_index + 1 if break_even_index is not None else 'nicht erreicht'}")
col3.metric("LCOE (€/kWh)", f"{(investment_total + opex_per_year * lifetime_years) / (stromertrag * lifetime_years):.3f}")

# Diagramm: Cashflow-Verlauf
st.subheader("📈 Cashflow-Verlauf")
fig, ax = plt.subplots()
ax.plot(years, cashflows, label="Jährlicher Cashflow")
ax.plot(years, kumulierte_cf, label="Kumulierte Cashflows")
if break_even_index is not None:
    ax.axvline(break_even_index + 1, color="red", linestyle="--", label="Break-even")
ax.set_xlabel("Jahr")
ax.set_ylabel("€")
ax.legend()
st.pyplot(fig)

# Teilnehmerquote-Analyse
st.subheader("👥 Teilnehmerquote vs. Strompreis")
quoten = np.arange(min_teilnehmer, max_teilnehmer + 1, 5)
preise = []
for q in quoten:
    teilnehmer_kwh = eigenverbrauch_kwh * (q / 100)
    preis = (fixkosten + variable_kosten_pro_kwh * teilnehmer_kwh) / teilnehmer_kwh
    preise.append(preis)

df_preise = pd.DataFrame({"Teilnehmerquote (%)": quoten, "Strompreis (€/kWh)": preise})
st.line_chart(df_preise.set_index("Teilnehmerquote (%)"))
st.dataframe(df_preise.style.format({"Strompreis (€/kWh)": "{:.3f}"}))
