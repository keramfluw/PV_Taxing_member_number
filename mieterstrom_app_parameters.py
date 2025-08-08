
class AnlagenParameter:
    def __init__(self, anlagengroesse_kwp, spezifischer_ertrag_kwh_kwp, eigenverbrauch_anteil,
                 reststrom_einspeisung, systemnutzungsgrad, lebensdauer_jahre):
        self.anlagengroesse_kwp = anlagengroesse_kwp
        self.spezifischer_ertrag_kwh_kwp = spezifischer_ertrag_kwh_kwp
        self.eigenverbrauch_anteil = eigenverbrauch_anteil
        self.reststrom_einspeisung = reststrom_einspeisung
        self.systemnutzungsgrad = systemnutzungsgrad
        self.lebensdauer_jahre = lebensdauer_jahre


class Investitionskosten:
    def __init__(self, pv_anlage, speicher, zaehlertechnik, installationskosten,
                 anschlusskosten, reserve, genehmigungen):
        self.pv_anlage = pv_anlage
        self.speicher = speicher
        self.zaehlertechnik = zaehlertechnik
        self.installationskosten = installationskosten
        self.anschlusskosten = anschlusskosten
        self.reserve = reserve
        self.genehmigungen = genehmigungen

    def gesamt(self):
        return sum([
            self.pv_anlage, self.speicher, self.zaehlertechnik, self.installationskosten,
            self.anschlusskosten, self.reserve, self.genehmigungen
        ])


class Betriebskosten:
    def __init__(self, wartung, versicherung, verwaltung, msb_kosten, dachpacht,
                 software_gebuehren, submetering):
        self.wartung = wartung
        self.versicherung = versicherung
        self.verwaltung = verwaltung
        self.msb_kosten = msb_kosten
        self.dachpacht = dachpacht
        self.software_gebuehren = software_gebuehren
        self.submetering = submetering

    def gesamt_jaehrlich(self):
        return sum([
            self.wartung, self.versicherung, self.verwaltung,
            self.msb_kosten, self.dachpacht, self.software_gebuehren, self.submetering
        ])


class Finanzierung:
    def __init__(self, fk_anteil, ek_anteil, kreditzins, tilgungsdauer, afa_satz, steuersatz):
        self.fk_anteil = fk_anteil
        self.ek_anteil = ek_anteil
        self.kreditzins = kreditzins
        self.tilgungsdauer = tilgungsdauer
        self.afa_satz = afa_satz
        self.steuersatz = steuersatz


class Einnahmen:
    def __init__(self, mieterstromerlöse, eeg_zuschlag, reststrom_einspeisung,
                 speicheroptimierung, netzdienliche_mehrerlöse):
        self.mieterstromerlöse = mieterstromerlöse
        self.eeg_zuschlag = eeg_zuschlag
        self.reststrom_einspeisung = reststrom_einspeisung
        self.speicheroptimierung = speicheroptimierung
        self.netzdienliche_mehrerlöse = netzdienliche_mehrerlöse

    def gesamt_jaehrlich(self):
        return sum([
            self.mieterstromerlöse, self.eeg_zuschlag, self.reststrom_einspeisung,
            self.speicheroptimierung, self.netzdienliche_mehrerlöse
        ])


class Wirtschaftlichkeit:
    def __init__(self, inflation, irr, cashflow_liste, break_even_jahr, lcoe, nutzungsquote):
        self.inflation = inflation
        self.irr = irr
        self.cashflow_liste = cashflow_liste
        self.break_even_jahr = break_even_jahr
        self.lcoe = lcoe
        self.nutzungsquote = nutzungsquote


class Sensitivitaet:
    def __init__(self, strompreissteigerung, zinsaenderung, beteiligungsquote,
                 pv_ertragsschwankung):
        self.strompreissteigerung = strompreissteigerung
        self.zinsaenderung = zinsaenderung
        self.beteiligungsquote = beteiligungsquote
        self.pv_ertragsschwankung = pv_ertragsschwankung


if __name__ == "__main__":
    # Beispielinitialisierung
    anlage = AnlagenParameter(100, 950, 0.6, 0.4, 0.95, 25)
    capex = Investitionskosten(70000, 10000, 5000, 15000, 3000, 5000, 2000)
    opex = Betriebskosten(1000, 500, 800, 1200, 300, 600, 400)
    finanzierung = Finanzierung(0.7, 0.3, 0.03, 20, 0.05, 0.30)
    einnahmen = Einnahmen(15000, 800, 1200, 500, 200)
    wirtschaftlichkeit = Wirtschaftlichkeit(0.02, 0.06, [5000]*25, 10, 0.12, 0.85)
    sensitivitaet = Sensitivitaet(0.03, 0.01, 0.75, 0.05)

    print(f"Gesamtkosten (CAPEX): {capex.gesamt():,.2f} €")
    print(f"Gesamte Betriebskosten (jährlich): {opex.gesamt_jaehrlich():,.2f} €")
    print(f"Gesamte Einnahmen (jährlich): {einnahmen.gesamt_jaehrlich():,.2f} €")
