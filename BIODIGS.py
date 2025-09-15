import streamlit as st
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Dimensionamiento de Biodigestores", layout="wide")

st.title("📊 Cálculo de dimensionamiento y viabilidad de biodigestores")

# ==============================
# FUNCIONES DE CÁLCULO
# ==============================

def calcular_ZGT(T):
    if 0 <= T <= 5:
        return "Zona bajo 0. T >5 °C requerida."
    elif 5 <= T <= 22:
        return "Altiplano - Rango Psicrofílico"
    elif 22 < T <= 32:
        return "Valle - Rango Mesofílico"
    elif 32 < T <= 40:
        return "Trópico - Rango Termofílico"
    elif 40 < T <= 56:
        return "Alta temperatura, control necesario - Termofílico"
    else:
        return "Temperatura fuera de rango (0-56 °C)"

def calcular_TRBB(T):
    if 0 <= T <= 5:
        return "Mantener T ≥7 °C"
    elif 5 <= T <= 22:
        return "Recomendado 10 a 28 °C"
    elif 22 < T <= 32:
        return "Recomendado 28 a 40 °C"
    elif 32 < T <= 40:
        return "Recomendado 40 a 75 °C"
    elif 40 < T <= 56:
        return "T ≤75 °C para fermentación termofílica"
    else:
        return "No viable económicamente"

def calcular_LANR(R, CED):
    if R == 0: return 0
    elif R == 1: return CED
    elif R == 2: return (CED + (CED * 0.05) * 2)
    elif R == 3: return (CED + (CED * 0.05) * 3)
    else: return None

def calcular_VUBR(TRH, CED, LANR):
    return (TRH * ((CED + LANR) / 1000) / 2.4) + (TRH * ((CED + LANR) / 1000))

def calcular_PBR(CED, EPBE, CSV, PBCSV):
    return (CED * CSV * PBCSV) if CSV > 0 else (CED * EPBE)

def calcular_CH4(PBR): return PBR * 0.65
def calcular_PER(PBR): return PBR * 2.4
def calcular_H2SR(PBR): return PBR * 0.0005
def calcular_ESBR(CED): return 0.98 * CED

# ==============================
# ENTRADAS DE USUARIO
# ==============================

st.sidebar.header("⚙️ Parámetros de entrada")

T = st.sidebar.number_input("Temperatura promedio de la zona (°C)", min_value=0.0, max_value=56.0, step=0.1)
TRH = st.sidebar.number_input("Tiempo de retención hidráulica (días)", min_value=1.0, step=1.0)
CED = st.sidebar.number_input("Carga diaria del biodigestor (Kg o L)", min_value=0.0, step=0.1)
R = st.sidebar.selectbox("Tipo de material", options=[0, 1, 2, 3], format_func=lambda x: {
    0: "0 - Líquidos",
    1: "1 - Muy húmedo",
    2: "2 - Poco húmedo",
    3: "3 - Restos vegetales / baja humedad"
}[x])
EPBE = st.sidebar.number_input("Equivalente de producción de biogás (m³/Kg)", min_value=0.0, step=0.01)
CSV = st.sidebar.number_input("Contenido de sólidos volátiles (%SV/Kg)", min_value=0.0, step=0.01)
PBCSV = st.sidebar.number_input("Producción de biogás a partir de SV (m³/Kg SV)", min_value=0.0, step=0.01)

# ==============================
# BOTÓN DE CÁLCULO
# ==============================

if st.sidebar.button("Calcular resultados"):
    TRBB = calcular_TRBB(T)
    ZGT = calcular_ZGT(T)
    LANR = calcular_LANR(R, CED)
    VUBR = round(calcular_VUBR(TRH, CED, LANR), 4)
    PBR = round(calcular_PBR(CED, EPBE, CSV, PBCSV), 4)
    CH4 = round(calcular_CH4(PBR), 4)
    PER = round(calcular_PER(PBR), 4)
    H2SR = round(calcular_H2SR(PBR), 4)
    ESBR = round(calcular_ESBR(CED), 4)

    st.subheader("📈 Resultados del dimensionamiento")
    st.write("**Zona geográfica y rango de fermentación (ZGT):**", ZGT)
    st.write("**Temperatura recomendada (TRBB):**", TRBB)
    st.write("**Razón de mezcla (LANR):**", LANR, "L")
    st.write("**Volumen útil biodigestor (VUBR):**", VUBR, "m³")
    st.write("**Producción de biogás (PBR):**", PBR, "m³")
    st.write("**Metano (CH4):**", CH4, "m³")
    st.write("**Producción energética (PER):**", PER, "kWh/m³")
    st.write("**Sulfuro de hidrógeno (H2SR):**", H2SR, "g/m³")
    st.write("**Efluentes biofertilizantes (ESBR):**", ESBR, "m³/día")

# ==============================
# SECCIONES EXTRA (TABLAS E IMÁGENES)
# ==============================

st.sidebar.header("📂 Secciones adicionales")
pagina = st.sidebar.radio("Ir a:", ["Principal", "Tabla 1", "Tabla 2", "Tabla 3", "Bioreactores"])

if pagina == "Tabla 1":
    st.subheader("📊 Tabla 1 - Tiempo de Retención Hidráulica")
    st.image("imagenes/TBL1.jpg", caption="Tabla 1", use_column_width=True)

elif pagina == "Tabla 2":
    st.subheader("📊 Tabla 2 - Equivalente de producción de biogás")
    st.image("imagenes/TBL2.jpg", caption="Tabla 2", use_column_width=True)

elif pagina == "Tabla 3":
    st.subheader("📊 Tabla 3 - Producción de biogás a partir de sólidos volátiles")
    st.image("imagenes/TBL3.jpg", caption="Tabla 3", use_column_width=True)

elif pagina == "Bioreactores":
    st.subheader("🧪 Tipos de bioreactores anaeróbicos")
    st.image("imagenes/Tipos de biodigestores.png", caption="Tipos de biodigestores", use_column_width=True)

else:
    st.subheader("📷 Imagen de referencia principal")
    st.image("imagenes/Características generales del biogás.png", caption="Características generales del biogás", use_column_width=True)

    st.markdown("""
    **REFERENCIAS**  
    - Casanovas, G., Della, F., Reymundo, F., & Serafini, R. (2019). *Guía teórico-práctica sobre el biogás y los biodigestores*. FAO.  
    - Pautrat Guerra, J. A. (2010). *Diseño de biodigestor y producción de biogás con excremento vacuno en la granja agropecuaria de Yauris*.  
    - Varnero, M. M. T. (2011). *Manual de biogás*. Minenergia-PNUD-FAO-GEF.  
    - Herrero, J. M. (2008). *Biodigestores familiares: Guía de diseño y manual de instalación*.  
    """)

