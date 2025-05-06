import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import requests

st.set_page_config(layout="wide")
st.title("🗺️ Viaggio in Corsica (Gaietta & Ste)")

# 1. Mappa originale invariata
mappa = folium.Map(location=[42.0396, 9.0129], zoom_start=8)
cluster = MarkerCluster().add_to(mappa)

# 2. Tappe principali (NESSUN CAMBIAMENTO)
tappe_principali = [
    {"luogo": "Bastia", "date": "9 luglio", "attivita": "Arrivo al porto (14:00)", "coords": [42.6973, 9.4509]},
    {"luogo": "Macinaggio", "date": "9 luglio", "attivita": "Pernottamento", "coords": [42.9639, 9.4533]},
    {"luogo": "Centuri", "date": "10 luglio", "attivita": "Pernottamento", "coords": [42.9636, 9.3589]},
    {"luogo": "Saint-Florent", "date": "11 luglio", "attivita": "Pernottamento", "coords": [42.6836, 9.3025]},
    {"luogo": "L'Île-Rousse", "date": "12-13 luglio", "attivita": "Pernottamento", "coords": [42.6333, 8.9333]},
    {"luogo": "Corte", "date": "14 luglio", "attivita": "Pernottamento", "coords": [42.3063, 9.1490]},
    {"luogo": "Propriano", "date": "15-16 luglio", "attivita": "Pernottamento", "coords": [41.6767, 8.9036]},
    {"luogo": "Bonifacio", "date": "17-18 luglio", "attivita": "Pernottamento", "coords": [41.3879, 9.1595]},
    {"luogo": "Porto-Vecchio", "date": "19-20 luglio", "attivita": "Pernottamento", "coords": [41.5912, 9.2795]},
]

# 3. Località secondarie MODIFICATE SOLO NELLE ICONE (stessa forma ma più piccole)
localita_secondarie = [
    {"luogo": "Barcaggio", "tipo": "spiaggia", "coords": [43.0100, 9.4155], "colore": "blue"},
    {"luogo": "Tamarone", "tipo": "spiaggia", "coords": [42.9757, 9.4547], "colore": "blue"},
    {"luogo": "Sentiero dei Doganieri", "tipo": "natura", "coords": [43.0014, 9.4351], "colore": "green"},
    {"luogo": "Saleccia", "tipo": "spiaggia", "coords": [42.7289, 9.2045], "colore": "blue"},
    {"luogo": "Lotu", "tipo": "spiaggia", "coords": [42.7201, 9.2334], "colore": "blue"},
    {"luogo": "Bodri", "tipo": "spiaggia", "coords": [42.6300, 8.9136], "colore": "blue"},
    {"luogo": "Ostriconi", "tipo": "spiaggia", "coords": [42.6640, 9.0600], "colore": "blue"},
    {"luogo": "Lozari", "tipo": "spiaggia", "coords": [42.6413, 9.0160], "colore": "blue"},
    {"luogo": "Pigna", "tipo": "borgo", "coords": [42.5996, 8.9030], "colore": "orange"},
    {"luogo": "Sant'Antonio", "tipo": "borgo", "coords": [42.5894, 8.9042], "colore": "orange"},
    {"luogo": "Gole della Restonica", "tipo": "natura", "coords": [42.2620, 9.0809], "colore": "green"},
    {"luogo": "Ajaccio", "tipo": "borgo", "coords": [41.9189, 8.7393], "colore": "orange"},
    {"luogo": "Cupabia", "tipo": "spiaggia", "coords": [41.7399, 8.7899], "colore": "blue"},
    {"luogo": "Isolella", "tipo": "spiaggia", "coords": [41.8473, 8.7640], "colore": "blue"},
    {"luogo": "Port de Chiavari", "tipo": "spiaggia", "coords": [41.8108, 8.7705], "colore": "blue"},
    {"luogo": "Ruppione", "tipo": "spiaggia", "coords": [41.8320, 8.7843], "colore": "blue"},
    {"luogo": "Scalinata del Re d'Aragona", "tipo": "borgo", "coords": [41.3864, 9.1568], "colore": "orange"},
    {"luogo": "Palombaggia", "tipo": "spiaggia", "coords": [41.5582, 9.3254], "colore": "blue"},
    {"luogo": "Piantarella", "tipo": "spiaggia", "coords": [41.3738, 9.2209], "colore": "blue"},
    {"luogo": "Rondinara", "tipo": "spiaggia", "coords": [41.4725, 9.2680], "colore": "blue"},
    {"luogo": "Santa Giulia", "tipo": "spiaggia", "coords": [41.5313, 9.2738], "colore": "blue"},
    {"luogo": "San Cipriano", "tipo": "spiaggia", "coords": [41.6392, 9.3492], "colore": "blue"},

]

# 4. Marker principali (ESATTAMENTE COME PRIMA)
for tappa in tappe_principali:
    popup = f"<b>{tappa['luogo']}</b><br><i>{tappa['date']}</i><br>{tappa['attivita']}"
    folium.Marker(
        location=tappa["coords"],
        popup=popup,
        tooltip=tappa["luogo"],
        icon=folium.Icon(color='red', icon='heart', prefix='fa') # Nessun icon_size per mantenere dimensioni default
    ).add_to(cluster)

for loc in localita_secondarie:
    # Assegna icone in base al tipo
    if loc['tipo'] == 'spiaggia':
        icon_html = '<i class="fa fa-water" style="color: white; font-size: 12px"></i>'
    elif loc['tipo'] == 'borgo':
        icon_html = '<i class="fa fa-home" style="color: white; font-size: 12px"></i>'
    else:  # natura
        icon_html = '<i class="fa fa-tree" style="color: white; font-size: 12px"></i>'

    # Crea un cerchio colorato con icona al centro
    folium.CircleMarker(
        location=loc["coords"],
        radius=10,  # Dimensione del cerchio
        color=loc["colore"],
        fill=True,
        fill_color=loc["colore"],
        fill_opacity=1,
        popup=f"<b>{loc['luogo']}</b><br>Tipo: {loc['tipo']}",
    ).add_to(mappa)

    # Aggiungi l'icona come overlay (usando DivIcon)
    folium.Marker(
        location=loc["coords"],
        icon=folium.DivIcon(
            html=f'<div style="display: flex; justify-content: center; align-items: center;">{icon_html}</div>',
            icon_size=(12, 12),
        ),
        z_index_offset=1000  # Assicura che l'icona sia sopra il cerchio
    ).add_to(mappa)

# 6. Percorsi e resto del codice (NESSUN CAMBIAMENTO)
def get_route_osrm(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 'Ok':
                coordinates = data['routes'][0]['geometry']['coordinates']
                return [[coord[1], coord[0]] for coord in coordinates]
    except:
        pass
    return [start, end]

for i in range(len(tappe_principali)-1):
    start = tappe_principali[i]["coords"]
    end = tappe_principali[i+1]["coords"]
    route = get_route_osrm(start, end)
    folium.PolyLine(
        route,
        color="red",
        weight=3,
        opacity=0.7,
        tooltip=f"Da {tappe_principali[i]['luogo']} a {tappe_principali[i+1]['luogo']}"
    ).add_to(mappa)

folium_static(mappa)

# Legenda
st.markdown("""
<style>
.legend-icon {
    display: inline-block;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    text-align: center;
    line-height: 20px;
    color: white;
    font-size: 10px;
    margin-right: 5px;
}
</style>

### Legenda:
- ❤️ Tappe principali (Pernottamenti)
- <span class="legend-icon" style="background: #1E90FF;">🌊</span> Spiagge
- <span class="legend-icon" style="background: #FFA500;">🏠</span> Borghi
- <span class="legend-icon" style="background: #32CD32;">🌳</span> Trekking
""", unsafe_allow_html=True)


# Descrizione dettagliata del viaggio
st.subheader("📝 Itinerario Dettagliato")
st.markdown("""
### Giorno 1 (9 luglio) - Arrivo a Macinaggio
**Arrivo al porto di Bastia** alle 14:00. Trasferimento verso nord lungo la costa orientale fino a Macinaggio, pittoresco villaggio di pescatori all'estremità nord del Capo Corso. 
Tempo libero per esplorare il porticciolo e le spiagge vicine. Cena tipica con prodotti locali.

### Giorno 2 (10 luglio) - Esplorando Capo Corso
Colazione e partenza per **Centuri**, passando per le splendide spiagge di **Barcaggio e Tamarone**. 
Pomeriggio dedicato al **Sentiero dei Doganieri**, con viste mozzafiato sulle scogliere. 
Rientro a Centuri per la cena a base di aragosta (specialità del luogo).

### Giorno 3 (11 luglio) - Saint-Florent e il Deserto degli Agriates  
**Mattino** dedicato alla scoperta di **Saint-Florent**, gioiello mediterraneo con il suo porticciolo bianco e le viuzze animate.  
**Pomeriggio** avventura verso il **Deserto degli Agriates**, raggiungendo in barca o 4x4 le spiagge di **Saleccia e Lotu**, lingue di sabbia bianca bagnate da acque cristalline.  

### Giorni 4-5 (12-13 luglio) - L'Île-Rousse e la Balagna  
**Esplorazione della costa nord-occidentale**:  
- Visita a **Calvi**, con la sua cittadella genovese e il vivace porto turistico  
- Relax sulle **spiagge di Bodri e Lozari**, acque turchesi incorniciate da pinete  
- Scoperta dei **villaggi arroccati** (Pigna, Sant'Antonino) tra botteghe artigiane e degustazioni di vini locali  
Pernottamento tra L'Île-Rousse e dintorni, tra il profumo del macchione e il rumore delle onde.

### Giorno 6 (14 luglio) - Corte e le Gole della Restonica  
**Immersione nella Corsica più autentica**:  
- Trekking alle **Gole della Restonica**, con bagno rinfrescante nei laghi montani **Melo e Capitello**  
Cena tipica in una "cantina" corsa, tra formaggi di pecora e castagne.

### Giorni 7-8 (15-16 luglio) - Tra Ajaccio e Propriano  
**Dal fascino napoleonico alle calette selvagge**:  
- Visita ad **Ajaccio**, tra la casa natale di Napoleone e il colorato mercato locale  
- Scoperta delle **spiagge incontaminate** di Campomoro e Cupabia  
Pernottamento a Propriano, con vista sul golfo illuminato.

### Giorni 9-10 (17-18 luglio) - Bonifacio, regina delle scogliere  
**Esplorazione della città-fortezza**:  
- Passeggiata lungo le **falesie calcaree**, sopra grotte marine blu cobalto  
- Discesa delle **scale del Re d'Aragona**, scavate nella roccia  

### Giorni 11-12 (19-20 luglio) - Porto-Vecchio e il paradiso sabbioso  
**Ultime giornate di mare**:  
- Mattinata tra le boutique e i caffè del **centro storico**  
- Pomeriggi di relax a **Palombaggia** e **Santa Giulia**, dove la sabbia è polvere di corallo  
- Tramonti rosso fuoco che tingono le isole Cerbicali  

### Giorno 13 (21 luglio) - Ritorno a Bastia  
**Chiusura del viaggio**:  
Breve visita alla **cittadella** e al **vecchio porto** di Bastia, dove i pescherecci scaricano il pesce del giorno.  
Ultimo caffè in Place Saint-Nicolas prima del rientro. 
""")

