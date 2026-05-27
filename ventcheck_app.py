import streamlit as st
import pandas as pd
import datetime

# CONFIGURACIÓN DE PÁGINA (LOOK UCI OSCURO)
st.set_page_config(
    page_title="VentCheck - Clínico",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# REINYECCIÓN DE ESTILOS CSS / HTML PARA TRASLADAR EL DISEÑO DE LA CAPTURA
st.markdown("""
    <style>
    /* Fondo global de la app en modo oscuro clínico */
    .stApp {
        background-color: #0E131F !important;
        color: #E2E8F0 !important;
    }
    
    /* Contenedores principales (Paneles de la captura) */
    .panel-clinical {
        background: #151C2C;
        border: 1px solid #232E46;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .panel-header {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748B;
        font-weight: bold;
        margin-bottom: 10px;
        border-bottom: 1px solid #232E46;
        padding-bottom: 5px;
    }
    
    /* Tipografías específicas */
    .data-highlight {
        color: #F59E0B;
        font-weight: bold;
    }
    
    /* Alertas de Riesgo Crítico (Cuentarrevoluciones Volutrauma) */
    .risk-box-red {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #EF4444;
        border-radius: 8px;
        padding: 12px;
        color: #FCA5A5;
        text-align: center;
        font-size: 13px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    .risk-box-green {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
        border-radius: 8px;
        padding: 12px;
        color: #A7F3D0;
        text-align: center;
        font-size: 13px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    /* Simulación de Gráfico de Barras de la Driving Pressure (Verde Maquet) */
    .bar-container {
        display: flex;
        align-items: flex-end;
        height: 60px;
        gap: 4px;
        margin: 15px 0;
    }
    .bar-green {
        flex: 1;
        background: linear-gradient(180deg, #10B981 0%, #059669 100%);
        border-radius: 2px 2px 0 0;
    }
    .bar-empty {
        flex: 1;
        background: #232E46;
        border-radius: 2px 2px 0 0;
    }
    
    /* Pestañas de navegación superiores customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #151C2C;
        padding: 8px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        border-radius: 4px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# PERSISTENCIA LOCAL DE LA BASE DE DATOS CIENTÍFICA
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        'Fecha_Hora', 'Cama', 'Sexo', 'Talla_cm', 'PCI_kg', 'Patologia',
        'Vt_Programado_ml', 'Vt_Real_ml_kg', 'PEEP_Programada', 'PEEP_Total',
        'Auto_PEEP', 'Pmeseta', 'Driving_Pressure', 'FiO2_Porcentaje', 'Estado_Seguridad'
    ])

# VARIABLES DE SESIÓN POR DEFECTO (Sincronizadas con la captura de pantalla)
if 'input_data' not in st.session_state:
    st.session_state.input_data = {
        'cama': 'Cama 4', 'sexo': 'Varón', 'talla': 182, 'patologia': 'EPOC / Obstructivo',
        'vt_prog': 450, 'fr': 12, 'flujo': 75, 'peep_prog': 10,
        'pmeseta': 19, 'ppico': 28, 'peep_total': 12, 'fio2': 60
    }

# FÓRMULA DEL PESO CORPORAL IDEAL (MANDATORIA)
def calcular_pci(sexo, talla):
    if sexo == "Varón":
        return round(50 + 2.3 * ((talla / 2.54) - 60), 1)
    else:
        return round(45.5 + 2.3 * ((talla / 2.54) - 60), 1)

# ENCABEZADO MINIMALISTA DE LA APP
st.markdown("<h2 style='text-align: center; color: #38BDF8; font-family: monospace; letter-spacing: 2px; margin-bottom: 20px;'>🫁 VENTCHECK OS</h2>", unsafe_allow_html=True)

# RENDERIZADO DE LAS 4 PESTAÑAS EXIGIDAS
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Dashboard de Resultados", 
    "⌨️ 2. Introducción de Datos", 
    "📚 3. Academia VentCheck", 
    "🗄️ 4. Histórico y Data Research"
])

# EXTRACCIÓN DE PARÁMETROS ACTIVOS
d = st.session_state.input_data
pci = calcular_pci(d['sexo'], d['talla'])
vt_relativo = round(d['vt_prog'] / pci, 2)
driving_pressure = d['pmeseta'] - d['peep_total']
auto_peep = max(0, d['peep_total'] - d['peep_prog'])

# -----------------------------------------------------------------------------------------
# PESTAÑA 1: DASHBOARD DE RESULTADOS (EL CLON DE TU CAPTURA DE PANTALLA)
# -----------------------------------------------------------------------------------------
with tab1:
    # PANEL 1: IDENTIFICACIÓN DEL PACIENTE
    st.markdown(f"""
    <div class="panel-clinical">
        <div class="panel-header">PATIENT PROFILE</div>
        <div style="font-size: 16px; font-family: monospace;">
            Género: <span style="color:#38BDF8;">{d['sexo']}</span> | 
            Estatura: <span style="color:#38BDF8;">{d['talla']} cm</span> | 
            <b>Predicted Body Weight (PBW): <span style="color:#10B981;">{pci} kg</span></b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # PANEL 2: MECÁNICA ALVEOLAR Y RIESGOS CRÍTICOS (DOS COLUMNAS IDÉNTICAS A LA IMAGEN)
    st.markdown('<div class="panel-clinical"><div class="panel-header">CRITICAL RISKS & ALVEOLAR MECHANICS</div>', unsafe_allow_html=True)
    
    # Datos leídos en texto arriba de los gráficos
    st.markdown(f"""
    <div style="font-family: monospace; font-size: 14px; margin-bottom: 15px; background: #0E131F; padding: 10px; border-radius: 6px; border: 1px solid #232E46;">
        PBW: <span class="data-highlight">{pci} kg</span> &nbsp;|&nbsp; 
        Vt: <span class="data-highlight">{d['vt_prog']} ml</span> &nbsp;|&nbsp; 
        PEEP Total: <span class="data-highlight">{d['peep_total']} cmH2O</span> &nbsp;|&nbsp; 
        Pmeseta: <span class="data-highlight">{d['pmeseta']} cmH2O</span> &nbsp;|&nbsp; 
        FiO2: <span class="data-highlight">{d['fio2']}%</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown(f"""
        <div style="background: #0E131F; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #232E46; height: 260px;">
            <div style="font-size: 12px; color: #94A3B8; font-weight: bold;">Vol/PCI (Vt/PBW)</div>
            <div style="font-size: 36px; font-weight: bold; margin-top: 20px; color: #EF4444;">{vt_relativo} <small style="font-size:14px;">ml/kg</small></div>
            <div style="color: #64748B; font-size: 11px; margin-top: 5px;">Rango óptimo EPOC: 5.0 - 6.0 ml/kg</div>
        """, unsafe_allow_html=True)
        
        # Alerta dinámica texturizada según peso relativo
        if vt_relativo > 7.0:
            st.markdown(f"<div class='risk-box-red'>Vt is {int((vt_relativo/6)*100)}% of target.<br>SEVERE VOLUTRAUMA RISK (EPOC)</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='risk-box-green'>Vt WITHIN PROTECTIVE RANGE</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_g2:
        # Simulación visual de las barras de distensibilidad Maquet
        barras_html = "".join(["<div class='bar-green'></div>" for _ in range(5)] + ["<div class='bar-empty'></div>" for _ in range(3)])
        
        st.markdown(f"""
        <div style="background: #0E131F; padding: 15px; border-radius: 8px; border: 1px solid #232E46; height: 260px;">
            <div style="font-size: 12px; color: #94A3B8; font-weight: bold; text-align: center;">MECÁNICA ALVEOLAR (Driving Pressure)</div>
            <div style="font-size: 12px; font-family: monospace; text-align: center; color: #A7F3D0; margin-top: 10px;">
                Pmeseta ({d['pmeseta']}) - PEEP Total ({d['peep_total']})
            </div>
            <div style="font-size: 28px; font-weight: bold; color: #10B981; text-align: center; margin-top: 5px;">= ΔP: {driving_pressure} cmH2O</div>
            <div class="bar-container">{barras_html}</div>
        """, unsafe_allow_html=True)
        
        if driving_pressure < 14:
            st.markdown(f"<div class='risk-box-green'>ΔP is {int((driving_pressure/14)*100)}% of limit (14). Safe.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='risk-box-red'>ΔP CRITICAL STRESS. ALVEOLAR DAMAGE.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True) # Cierre panel
    
    # PANEL 3: INTERCAMBIO DE GASES Y FiO2 (Gráfica de barras simulada en CSS)
    st.markdown('<div class="panel-clinical"><div class="panel-header">OXIGENACIÓN (FiO2 vs Target)</div>', unsafe_allow_html=True)
    
    col_o1, col_o2 = st.columns([3, 1])
    with col_o1:
        # Gráfico CSS nativo simulando histogramas Maquet
        st.markdown(f"""
        <div style="background: #0E131F; padding: 20px; border-radius: 8px; border: 1px solid #232E46; height: 140px; display: flex; align-items: flex-end; gap: 15px;">
            <div style="flex:1; background: #232E46; height: 40px; border-radius: 4px;"></div>
            <div style="flex:1; background: #232E46; height: 50px; border-radius: 4px;"></div>
            <div style="flex:1; background: #F59E0B; height: 90px; border-radius: 4px; border: 2px solid #EF4444; box-shadow: 0 0 10px rgba(239,68,68,0.5);"></div>
            <div style="flex:1; background: #F59E0B; height: 100px; border-radius: 4px;"></div>
            <div style="font-family: monospace; font-size: 12px; color: #94A3B8; margin-left: 20px; align-self: center;">
                <span style="color: #F59E0B;">●</span> Current FiO2: {d['fio2']}%<br>
                <span style="color: #10B981;">●</span> EPOC Target: 30% - 40%
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_o2:
        if d['fio2'] > 40 and "EPOC" in d['patologia']:
            st.markdown(f"""
            <div class='risk-box-red' style="height: 140px; display: flex; flex-direction: column; justify-content: center; margin-top: 0;">
                🚨 ALERTA HIPEROXIA<br><br>High FiO2 ({d['fio2']}%) Risks Haldane / Shunt. Consider reduction.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='risk-box-green' style='height:140px;'>FiO2 CONTROLADA</div>", unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # BOTÓN DE GUARDADO PRINCIPAL (EL DE TU CAPTURA DE PANTALLA)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 CONFIRMAR Y GUARDAR REGISTRO CLÍNICO", use_container_width=True):
        es_seguro = "Protector" if (driving_pressure < 14 and d['pmeseta'] <= 30 and vt_relativo <= 6) else "Estrés Mecánico"
        nuevo_registro = pd.DataFrame([{
            'Fecha_Hora': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'Cama': d['cama'], 'Sexo': d['sexo'], 'Talla_cm': d['talla'], 'PCI_kg': pci, 'Patologia': d['patologia'],
            'Vt_Programado_ml': d['vt_prog'], 'Vt_Real_ml_kg': vt_relativo, 'PEEP_Programada': d['peep_prog'],
            'PEEP_Total': d['peep_total'], 'Auto_PEEP': auto_peep, 'Pmeseta': d['pmeseta'],
            'Driving_Pressure': driving_pressure, 'FiO2_Porcentaje': d['fio2'], 'Estado_Seguridad': es_seguro
        }])
        st.session_state.db = pd.concat([st.session_state.db, nuevo_registro], ignore_index=True)
        st.success(f"¡Hecho! Los índices de la {d['cama']} se han volcado a la base de datos de investigación.")

# -----------------------------------------------------------------------------------------
# PESTAÑA 2: INTRODUCCIÓN DE DATOS (EL MOTOR DE ENTRADA MANUAL)
# -----------------------------------------------------------------------------------------
with tab2:
    st.markdown('<div class="panel-clinical"><div class="panel-header">ENTRADA MANUAL DE PARÁMETROS</div>', unsafe_allow_html=True)
    
    col_in1, col_in2 = st.columns(2)
    
    with col_in1:
        st.subheader("Datos de Cabecera")
        cama = st.text_input("Código de Cama / Paciente", value=d['cama'])
        sexo = st.radio("Sexo para cálculo de PCI", ["Varón", "Mujer"], index=0 if d['sexo']=="Varón" else 1, horizontal=True)
        talla = st.slider("Talla del paciente (cm)", min_value=140, max_value=210, value=d['talla'])
        patologia = st.selectbox("Fenotipo Fisiopatológico", ["EPOC / Obstructivo", "SDRA / Restrictivo", "Neurocrítico", "Estándar Protector"], index=0)
        
    with col_in2:
        st.subheader("Mecánica e Índices")
        vt_prog = st.number_input("Vt Programado (ml)", min_value=200, max_value=800, value=d['vt_prog'])
        peep_prog = st.number_input("PEEP Extrínseca Programada (cmH2O)", min_value=0, max_value=25, value=d['peep_prog'])
        pmeseta = st.number_input("Presión Meseta (Pausa Inspiratoria) (cmH2O)", min_value=0, max_value=50, value=d['pmeseta'])
        peep_total = st.number_input("PEEP Total (Pausa Espiratoria) (cmH2O)", min_value=0, max_value=30, value=d['peep_total'])
        fio2 = st.number_input("FiO2 (%)", min_value=21, max_value=100, value=d['fio2'])
        
    if st.button("⚡ PROCESAR AJUSTES Y ACTUALIZAR DASHBOARD", use_container_width=True):
        st.session_state.input_data = {
            'cama': cama, 'sexo': sexo, 'talla': talla, 'patologia': patologia,
            'vt_prog': vt_prog, 'fr': d['fr'], 'flujo': d['flujo'], 'peep_prog': peep_prog,
            'pmeseta': pmeseta, 'ppico': d['ppico'], 'peep_total': peep_total, 'fio2': fio2
        }
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# PESTAÑA 3: ACADEMIA VENTCHECK (EL MÓDULO DE APRENDIZAJE)
# -----------------------------------------------------------------------------------------
with tab3:
    st.markdown('<div class="panel-clinical"><div class="panel-header">ACADEMIA VENTCHECK: REPASO CIENTÍFICO</div>', unsafe_allow_html=True)
    
    with st.expander("🎓 1. Fisiología en EPOC: Por qué la FiO2 alta retiene CO2"):
        st.markdown("""
        La creencia clásica decía que el exceso de oxígeno anulaba el estímulo respiratorio cerebral. Hoy sabemos que los mecanismos principales son vasculares:
        * **Efecto Haldane:** Al hiperoxigenar la hemoglobina, esta disminuye de golpe su capacidad de transportar $CO_2$. El gas se disuelve en el plasma disparando la acidosis y la hipercapnia en sangre.
        * **Abolición de la Vasoconstricción Pulmonar Hipóxica (VPH):** El pulmón del EPOC cierra de forma inteligente las arterias de las zonas destruidas para desviar la sangre a zonas sanas. Si pones demasiada $FiO_2$, dilatas esos vasos cerrados y la sangre vuelve a pasar por zonas muertas (efecto Shunt), bloqueando la salida del $CO_2$.
        * **Diana Asistencial:** Mantener siempre la saturación en el monitor entre el **88% y 92%**.
        """)
        
    with st.expander("📉 2. El Factor Predictivo Clave: Driving Pressure"):
        st.markdown("""
        La **Presión de Conducción ($\Delta P = P_{\text{meseta}} - P_{\text{PEEP total}}$)** nos indica el nivel de deformación y estrés físico que sufre el pulmón elástico remanente funcional del paciente.
        * La evidencia científica exige mantenerla **por debajo de 14 cmH2O**.
        * Todo valor superior es un predictor independiente de daño tisular y mortalidad en la UCI.
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# PESTAÑA 4: HISTÓRICO Y DATA RESEARCH (EXPORTACIÓN DIRECTA A EXCEL)
# -----------------------------------------------------------------------------------------
with tab4:
    st.markdown('<div class="panel-clinical"><div class="panel-header">REGISTRO CIENTÍFICO Y EXPORTACIÓN DE LA UNIDAD</div>', unsafe_allow_html=True)
    
    if st.session_state.db.empty:
        st.info("La base de datos local está vacía. Introduce parámetros en la Pestaña 2 y haz clic en 'Confirmar y Guardar' en la Pestaña 1.")
    else:
        st.dataframe(st.session_state.db, use_container_width=True)
        
        # Generador en memoria del archivo Excel nativo (.xlsx) para SPSS o R
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.db.to_excel(writer, index=False, sheet_name='Estudio_UCI')
        excel_data = output.getvalue()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 DESCARGAR BASE DE DATOS EN FORMATO EXCEL (.XLSX) PARA ESTUDIO CIENTÍFICO",
            data=excel_data,
            file_name=f"VentCheck_DataResearch_{datetime.date.today().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    st.markdown('</div>', unsafe_allow_html=True)