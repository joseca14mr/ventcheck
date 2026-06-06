import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# CONFIGURACIÓN DE PÁGINA PROFESIONAL MULTIPLATAFORMA MULTI-DEVICE
st.set_page_config(
    page_title="VentCheck",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# REINYECCIÓN DE ESTILOS CSS AVANZADOS (Entorno de Monitorización UCI Premium)
st.markdown("""
    <style>
    /* Fondo global y tipografía limpia electromédica */
    .stApp {
        background-color: #0B0F19 !important;
        color: #E2E8F0 !important;
    }
    
    /* Contenedor responsivo centralizado para evitar estiramientos elásticos en PC */
    .main-responsive-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 0 10px;
    }
    
    /* Paneles clínicos oscuros con relieve translúcido */
    .panel-clinical {
        background: linear-gradient(135deg, #131A2A 0%, #172034 100%);
        border: 1px solid #24324F;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
    }
    
    .panel-header {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #64748B;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 1px solid #24324F;
        padding-bottom: 6px;
    }
    
    .section-title-sub {
        font-size: 13px;
        color: #38BDF8;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 10px;
    }
    
    .data-highlight {
        color: #38BDF8;
        font-weight: bold;
    }
    
    /* Botonera de pestañas enmarcada y centrada de forma multiplataforma */
    .nav-box-centered {
        background: #131A2A;
        border: 1px solid #24324F;
        border-radius: 10px;
        padding: 6px 12px;
        max-width: 620px;
        margin: 0 auto 20px auto;
        box-shadow: 0 4px 14px rgba(0,0,0,0.3);
    }
    
    /* Cuadro de Alertas de Gasometría */
    .gaso-alert-card {
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        font-family: monospace;
        font-size: 14px;
        font-weight: bold;
        letter-spacing: 0.5px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
        margin-top: 10px;
        margin-bottom: 15px;
    }
    
    /* Barra elástica de pH */
    .ph-gauge-bg {
        background: linear-gradient(90deg, #EF4444 0%, #F59E0B 35%, #10B981 45%, #10B981 55%, #F59E0B 65%, #38BDF8 100%);
        border-radius: 9px;
        height: 14px;
        width: 100%;
        position: relative;
        margin-top: 15px;
        margin-bottom: 8px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }
    .ph-gauge-pointer {
        position: absolute;
        top: -4px;
        width: 6px;
        height: 22px;
        background-color: #FFFFFF;
        border-radius: 2px;
        box-shadow: 0 0 8px rgba(255,255,255,0.8), 0 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Cajas contenedoras elásticas para las Métricas de Seguridad circulares */
    .security-metric-box {
        background: rgba(11, 15, 25, 0.5);
        border: 1px solid #24324F;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .academic-text {
        font-size: 14px;
        line-height: 1.5;
        color: #CBD5E1;
        text-align: justify;
    }
    .academic-subtitle {
        font-size: 15px;
        color: #38BDF8;
        font-weight: bold;
        margin-top: 12px;
        margin-bottom: 8px;
        border-left: 3px solid #38BDF8;
        padding-left: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# INICIALIZACIÓN DE LA BASE DE DATOS LOCAL DE LA SESIÓN (DATA)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        'Fecha_Hora', 'Paciente_ID', 'Sexo', 'Talla_cm', 'PCI_kg', 'Patologias', 'Modo_Ventilatorio',
        'Parametro_Volumen_ml', 'FR_Programada_rpm', 'PEEP_Programada_cmH2O', 'FiO2_Porcentaje',
        'Presion_Pico_cmH2O', 'PEEP_Total_cmH2O', 'Compliance_Estatica_ml_cmH2O', 'Elastancia_cmH2O_L',
        'Ri_cmH2O_L_s', 'Re_cmH2O_L_s', 'Tc_segundos', 'Ppausa_cmH2O', 'Flujo_Inspiratorio_L_min',
        'Vt_Real_ml_kg_PCI', 'Driving_Pressure_cmH2O', 'Auto_PEEP_cmH2O',
        'Mechanical_Power_J_min', 'Oxigenacion_Metodo', 'Oxigenacion_Valor_Entrada', 'Indice_Oxigenacion_Calculado',
        'SDRA_Clasificacion', 'Weaning_Evaluado', 'FR_Espontanea_rpm', 'P01_cmH2O', 'Tobin_RSBI', 
        'Weaning_Resultado', 'Soporte_Posterior', 'Causa_Fracaso', 'Rox_Indice', 'Estado_Seguridad'
    ])

# VALORES DE ENTRADA TEMPORALES DE LA SESIÓN ACTIVA
if 'input_data' not in st.session_state:
    st.session_state.input_data = {
        'cama': 'Paciente 1', 'sexo': 'Varón', 'talla': 175.0, 'patologias': ['Estándar Protector'],
        'modo': 'Controlado por Volumen (VCV)', 'vt_prog': 420.0, 'fr': 14.0, 
        'peep_prog': 8.0, 'ppico': 26.0, 'peep_total': 9.5, 'fio2': 40.0,
        'c_stat': 0.0, 'elastancia': 0.0, 'ri': 0.0, 're': 12.0, 'tc': 0.6, 'ppausa': 21.0, 'flujo_insp': 60.0,
        'disp_gaso': 'No (Evaluación por SAFI)', 'ox_val': 95.0, 'eval_weaning': 'No', 'fr_esp': 20.0, 'p01': 2.0,
        'weaning_res': 'En proceso', 'soporte_post': 'No aplica', 'causa_fracaso': 'No aplica', 'fr_rox': 20.0
    }

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Valores"

def calcular_pci(sexo, talla):
    base = 50.0 if sexo == "Varón" else 45.5
    return round(base + 2.3 * ((float(talla) / 2.54) - 60.0), 1)

# ENTRADA AL CONTENEDOR RESPONSIVO GLOBAL
st.markdown('<div class="main-responsive-container">', unsafe_allow_html=True)

# ENCABEZADO DE SOFTWARE
st.markdown("<h3 style='text-align: center; color: #38BDF8; font-family: monospace; letter-spacing: 3px; margin-top: 5px; margin-bottom: 12px;'>VENTCHECK</h3>", unsafe_allow_html=True)

d = st.session_state.input_data

# ENRUTADOR DE PESTAÑAS ENMARCADO Y CENTRADO MULTIPLATAFORMA
st.markdown('<div class="nav-box-centered">', unsafe_allow_html=True)
tab_options = ["Valores", "Resultados", "Gasometría", "Academia", "Data"]
chosen_tab = st.radio("Navegación Sistema", tab_options, index=tab_options.index(st.session_state.active_tab), horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = chosen_tab
st.markdown('</div>', unsafe_allow_html=True)

# PROCESAMIENTO Y MATEMÁTICA CLÍNICA DE CONTROL (Floats estrictos de rango elástico)
pci = float(calcular_pci(d['sexo'], d['talla']))
vt_relativo = round(float(d['vt_prog']) / pci, 2)
presion_elastica_ref = float(d['ppausa'])
driving_pressure = round(presion_elastica_ref - float(d['peep_total']), 1)
auto_peep = round(max(0.0, float(d['peep_total']) - float(d['peep_prog'])), 1)

# ASIGNACIÓN DINÁMICA DE UMBRALES DE SEGURIDAD SEGÚN ANTECEDENTE
es_obstructivo = any("EPOC" in p or "Obstructivo" in p for p in d['patologias'])
if es_obstructivo:
    min_vt, max_vt = 5.0, 6.0
    min_fio2, max_fio2 = 21.0, 40.0
    vt_rango_texto = "(Normal: 5.0 - 6.0 ml/kg PBW)"
    fio2_rango_texto = "(Normal: 21% - 40%)"
else:
    min_vt, max_vt = 6.0, 8.0
    min_fio2, max_fio2 = 21.0, 60.0
    vt_rango_texto = "(Normal: 6.0 - 8.0 ml/kg PBW)"
    fio2_rango_texto = "(Normal: 21% - 60%)"

# -----------------------------------------------------------------------------------------
# PESTAÑA: VALORES
# -----------------------------------------------------------------------------------------
if chosen_tab == "Valores":
    st.markdown('<div class="panel-clinical"><div class="panel-header">REGISTRO CIENTÍFICO DE DATOS</div>', unsafe_allow_html=True)
    
    col_ob1, col_ob2 = st.columns([1, 1])
    
    with col_ob1:
        st.markdown("<div class='section-title-sub'>Filiación y Datos del Paciente</div>", unsafe_allow_html=True)
        cama_in = st.text_input("ID Paciente / Cama", value=d['cama'])
        sexo_in = st.radio("Sexo biológico (Peso Ideal)", ["Varón", "Mujer"], index=0 if d['sexo']=="Varón" else 1, horizontal=True)
        
        # Modificación elástica: Talla integrada en number_input para evitar cierres táctiles accidentales por gestos en móvil
        talla_in = st.number_input("Talla del paciente (cm)", min_value=140.0, max_value=220.0, value=float(d['talla']), step=0.5)
        
        patologias_in = st.multiselect(
            "Patología / Síndrome",
            ["Estándar Protector", "SDRA / Restrictivo", "EPOC / Obstructivo", "Neurocrítico", "Neumonía"],
            default=d['patologias']
        )
        if not patologias_in:
            patologias_in = ["Estándar Protector"]

    with col_ob2:
        st.markdown("<div class='section-title-sub'>Programación del Respirador</div>", unsafe_allow_html=True)
        modo_in = st.selectbox("Modo de Ventilación", ["Controlado por Volumen (VCV)", "Controlado por Presión (PCV)"], index=0 if d['modo'] == "Controlado por Volumen (VCV)" else 1)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("<span style='font-size:12px; color:#64748B;'>VENTILACIÓN</span>", unsafe_allow_html=True)
            if modo_in == "Controlado por Volumen (VCV)":
                vt_prog_in = st.number_input("Volumen Corriente Programado - Vt (ml)", min_value=100.0, max_value=900.0, value=float(d['vt_prog']), step=10.0)
            else:
                vt_prog_in = st.number_input("Volumen Corriente Real Espirado - Vte (ml)", min_value=100.0, max_value=900.0, value=float(d['vt_prog']), step=10.0)
            fr_in = st.number_input("Frecuencia Respiratoria - FR (rpm)", min_value=4.0, max_value=45.0, value=float(d['fr']), step=1.0)
            
        with col_p2:
            st.markdown("<span style='font-size:12px; color:#64748B;'>OXIGENACIÓN</span>", unsafe_allow_html=True)
            fio2_in = st.number_input("Fracción Inspirada de Oxígeno - FiO2 (%)", min_value=21.0, max_value=100.0, value=float(d['fio2']), step=1.0)
            peep_prog_in = st.number_input("PEEP Programada (cmH2O)", min_value=0.0, max_value=30.0, value=float(d['peep_prog']), step=0.5)

    st.markdown("<hr style='border-color:#24324F; margin:10px 0;'>", unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
        st.markdown("<div class='section-title-sub'>Mediciones Dinámicas</div>", unsafe_allow_html=True)
        ppico_in = st.number_input("Presión Pico Máxima (cmH2O)", min_value=0.0, max_value=70.0, value=float(d['ppico']), step=0.5)
        flujo_insp_in = st.number_input("Flujo Inspiratorio (L/min)", min_value=10.0, max_value=120.0, value=float(d['flujo_insp']), step=5.0)
    
    with col_m2:
        st.markdown("<div class='section-title-sub'>Mediciones estáticas</div>", unsafe_allow_html=True)
        
        # Fila 1: Parámetros elásticos principales
        col_r1_1, col_r1_2, col_r1_3, col_r1_4 = st.columns(4)
        with col_r1_1:
            peep_total_in = st.number_input("Peep Total", min_value=0.0, max_value=40.0, value=float(d['peep_total']), step=0.5)
        with col_r1_2:
            ppausa_in = st.number_input("Pmeseta/Ppausa/Pplat", min_value=0.0, max_value=60.0, value=float(d['ppausa']), step=0.5)
        with col_r1_3:
            c_stat_in = st.number_input("Compliance", min_value=0.0, max_value=150.0, value=float(d['c_stat']), step=1.0)
        with col_r1_4:
            elastancia_in = st.number_input("Elastancia", min_value=0.0, max_value=100.0, value=float(d['elastancia']), step=1.0)
            
        # Fila 2: Dinámica de flujo y constantes
        col_r2_1, col_r2_2, col_r2_3, col_r2_4 = st.columns(4)
        with col_r2_1:
            ri_in = st.number_input("Rins", min_value=0.0, max_value=100.0, value=float(d['ri']), step=0.5)
        with col_r2_2:
            re_in = st.number_input("Respt", min_value=0.0, max_value=100.0, value=float(d['re']), step=0.5)
        with col_r2_3:
            tc_in = st.number_input("TC", min_value=0.0, max_value=5.0, value=float(d['tc']), step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

    # MÓDULOS AVANZADOS EN VALORES
    st.markdown('<div class="panel-clinical"><div class="panel-header">MÓDULOS AVANZADOS</div>', unsafe_allow_html=True)
    col_op1, col_op2 = st.columns([1, 1])
    
    with col_op1:
        st.markdown("<div class='section-title-sub'>Oxigenación e Intercambio</div>", unsafe_allow_html=True)
        disp_gaso_in = st.selectbox("Método de Evaluación", ["No (Evaluación por SAFI)", "Sí (Evaluación por PAFI)"], index=0 if "No" in d['disp_gaso'] else 1)
        if "Sí" in disp_gaso_in:
            ox_val_in = st.number_input("PaO2 Arterial (mmHg)", min_value=30.0, max_value=500.0, value=80.0 if d['ox_val'] == 95.0 else float(d['ox_val']), step=1.0)
        else:
            ox_val_in = st.number_input("Saturación Periférica - SatO2 (%)", min_value=30.0, max_value=100.0, value=float(d['ox_val']) if float(d['ox_val'])<=100.0 else 95.0, step=1.0)

    with col_op2:
        st.markdown("<div class='section-title-sub'>Esfuerzo Muscular y Weaning</div>", unsafe_allow_html=True)
        eval_weaning_in = st.selectbox("¿Evaluar Weaning?", ["No", "Sí"], index=0 if d['eval_weaning'] == "No" else 1)
        
        if eval_weaning_in == "Sí":
            fr_esp_in = st.number_input("FR Espontánea (rpm)", min_value=0.0, max_value=60.0, value=float(d['fr_esp']), step=1.0)
            p01_in = st.number_input("Presión de Oclusión - P0.1 (cmH2O)", min_value=0.0, max_value=20.0, value=float(d['p01']), step=0.1)
            weaning_res_in = st.selectbox("Resultado Weaning", ["En proceso", "Éxito de la desconexión", "Fracaso de la desconexión"], index=["En proceso", "Éxito de la desconexión", "Fracaso de la desconexión"].index(d['weaning_res']))
            soporte_post_in = st.selectbox("Soporte de Oxigenación Posterior", ["No aplica", "Gafas de oxígeno convencionales", "Mascarilla Venturi (Ventimask)", "Cánula Nasal de Alto Flujo (CNAF)", "Ventilación No Invasiva (VNI)"], index=["No aplica", "Gafas de oxígeno convencionales", "Mascarilla Venturi (Ventimask)", "Cánula Nasal de Alto Flujo (CNAF)", "Ventilación No Invasiva (VNI)"].index(d['soporte_post']))
            if soporte_post_in == "Cánula Nasal de Alto Flujo (CNAF)":
                fr_rox_in = st.number_input("FR del Paciente en CNAF (Índice ROX)", min_value=8.0, max_value=50.0, value=float(d['fr_rox']), step=1.0)
            else: fr_rox_in = 0.0
            causa_fracaso_in = st.selectbox("Causa del Fracaso", ["Exceso de trabajo respiratorio / Fatiga", "Inestabilidad hemodinámica", "Deterioro neurológico", "Ansiedad / Agitación"], index=0) if weaning_res_in == "Fracaso de la desconexión" else "No aplica"
        else:
            fr_esp_in = 0.0; p01_in = 0.0; fr_rox_in = 0.0; weaning_res_in = "No aplica"; soporte_post_in = "No aplica"; causa_fracaso_in = "No aplica"

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("PROCESAR CÁLCULOS E IR A RESULTADOS", use_container_width=True):
        st.session_state.input_data = {
            'cama': cama_in, 'sexo': sexo_in, 'talla': talla_in, 'patologias': patologias_in,
            'modo': modo_in, 'vt_prog': vt_prog_in, 'fr': fr_in, 'peep_prog': peep_prog_in, 
            'ppico': ppico_in, 'peep_total': peep_total_in, 'fio2': fio2_in, 'flujo_insp': flujo_insp_in,
            'c_stat': c_stat_in, 'elastancia': elastancia_in, 'ri': ri_in, 're': re_in, 'tc': tc_in, 'ppausa': ppausa_in,
            'disp_gaso': disp_gaso_in, 'ox_val': ox_val_in, 'eval_weaning': eval_weaning_in,
            'fr_esp': fr_esp_in, 'p01': p01_in, 'weaning_res': weaning_res_in, 'soporte_post': soporte_post_in, 'causa_fracaso': causa_fracaso_in, 'fr_rox': fr_rox_in
        }
        
        # Matemáticas puras en segundo plano para persistencia de la base de datos
        pci_g = float(calcular_pci(sexo_in, talla_in))
        vt_rel_g = round(float(vt_prog_in) / pci_g, 2)
        dp_g = round(float(ppausa_in) - float(peep_total_in), 1)
        apeep_g = round(max(0.0, float(peep_total_in) - float(peep_prog_in)), 1)
        final_cstat = round(float(vt_prog_in) / dp_g, 1) if (c_stat_in == 0.0 and dp_g > 0) else c_stat_in
        final_elastancia = round(1000.0 / final_cstat, 1) if (elastancia_in == 0.0 and final_cstat > 0) else elastancia_in
        final_ri = round((float(ppico_in) - float(ppausa_in)) / (float(flujo_insp_in) / 60.0), 1) if (ri_in == 0.0 and modo_in == "Controlado por Volumen (VCV)" and flujo_insp_in > 0) else ri_in
        m_power_g = round(0.0007 * float(vt_prog_in) * float(fr_in) * (float(ppico_in) - (dp_g / 2.0)), 2)
        ind_ox_g = round(float(ox_val_in) / (float(fio2_in) / 100.0), 1)
        sdra_cat = "No aplica"
        if any("SDRA" in p or "Neumonía" in p for p in patologias_in) and "Sí" in disp_gaso_in:
            if ind_ox_g < 100.0: sdra_cat = "Severo"
            elif ind_ox_g < 200.0: sdra_cat = "Moderado"
            elif ind_ox_g <= 300.0: sdra_cat = "Leve"
        tobin_g = round(float(fr_esp_in) / (float(vt_prog_in) / 1000.0), 1) if (eval_weaning_in == "Sí" and vt_prog_in > 0) else 0.0
        rox_g = round(ind_ox_g / float(fr_rox_in), 2) if (soporte_post_in == "Cánula Nasal de Alto Flujo (CNAF)" and fr_rox_in > 0) else 0.0
        es_seguro_g = "Estrategia Protectora" if (dp_g < 14.0 and ppausa_in <= 30.0) else "Estrés Alveolar Elevado"
        
        nuevo_registro = pd.DataFrame([{
            'Fecha_Hora': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 'Paciente_ID': cama_in, 'Sexo': sexo_in, 'Talla_cm': talla_in, 'PCI_kg': pci_g, 'Patologias': ", ".join(patologias_in), 'Modo_Ventilatorio': modo_in, 'Parametro_Volumen_ml': vt_prog_in, 'FR_Programada_rpm': fr_in, 'PEEP_Programada_cmH2O': peep_prog_in, 'FiO2_Porcentaje': fio2_in, 'Presion_Pico_cmH2O': ppico_in, 'Presion_Meseta_cmH2O': ppausa_in, 'PEEP_Total_cmH2O': peep_total_in, 'Compliance_Estatica_ml_cmH2O': final_cstat, 'Elastancia_cmH2O_L': final_elastancia, 'Ri_cmH2O_L_s': final_ri, 'Re_cmH2O_L_s': re_in, 'Tc_segundos': tc_in, 'Ppausa_cmH2O': ppausa_in, 'Flujo_Inspiratorio_L_min': flujo_insp_in, 'Vt_Real_ml_kg_PCI': vt_rel_g, 'Driving_Pressure_cmH2O': dp_g, 'Auto_PEEP_cmH2O': apeep_g, 'Mechanical_Power_J_min': m_power_g, 'Oxigenacion_Metodo': "PAFI" if "Sí" in disp_gaso_in else "SAFI", 'Oxigenacion_Valor_Entrada': ox_val_in, 'Indice_Oxigenacion_Calculado': ind_ox_g, 'SDRA_Clasificacion': sdra_cat, 'Weaning_Evaluado': eval_weaning_in, 'FR_Espontanea_rpm': fr_esp_in, 'P01_cmH2O': p01_in, 'Tobin_RSBI': tobin_g, 'Weaning_Resultado': weaning_res_in, 'Soporte_Posterior': soporte_post_in, 'Causa_Fracaso': causa_fracaso_in, 'Rox_Indice': rox_g, 'Estado_Seguridad': es_seguro_g
        }])
        st.session_state.db = pd.concat([st.session_state.db, nuevo_registro], ignore_index=True)
        st.session_state.active_tab = "Resultados"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# PESTAÑA: RESULTADOS (CON MODELO ANATÓMICO Y METRICAS EN RELLENO ALVEOLAR CIRCULAR)
# -----------------------------------------------------------------------------------------
elif chosen_tab == "Resultados":
    compliance_estatica = float(d['c_stat']) if float(d['c_stat']) > 0 else (round(float(d['vt_prog']) / driving_pressure, 1) if driving_pressure > 0 else 0.0)
    elastancia_calculada = float(d['elastancia']) if float(d['elastancia']) > 0 else (round(1000.0 / compliance_estatica, 1) if compliance_estatica > 0 else 0.0)
    ri_calculada = float(d['ri']) if float(d['ri']) > 0 else (round((float(d['ppico']) - float(d['ppausa'])) / (float(d['flujo_insp']) / 60.0), 1) if (d['modo'] == "Controlado por Volumen (VCV)" and float(d['flujo_insp']) > 0) else 0.0)
    mechanical_power = round(0.0007 * float(d['vt_prog']) * float(d['fr']) * (float(d['ppico']) - (driving_pressure / 2.0)), 2)
    indice_ox = round(float(d['ox_val']) / (float(d['fio2']) / 100.0), 1)

    # Lógica cromática elástica para el Mapa Anatómico Principal
    if driving_pressure >= 14.0 or mechanical_power >= 17.0:
        lung_color, stroke_glow, text_biomapa = "#EF4444", "#EF4444", "ALERTA: CRITERIOS DE DAÑO MECÁNICO ACTIVO (SOBREDISTENSIÓN)"
        lung_opacity = "0.75"
    elif driving_pressure >= 12.0:
        lung_color, stroke_glow, text_biomapa = "#F59E0B", "#F59E0B", "PRECAUCIÓN: BAJA DISTENSIBILIDAD PARENQUIMATOSA DEL SISTEMA"
        lung_opacity = "0.55"
    else:
        lung_color, stroke_glow, text_biomapa = "#10B981", "#10B981", "PULMÓN PROTEGIDO: ESTRATEGIA DE RECRUTAMIENTO ALVEOLAR ÓPTIMA"
        lung_opacity = "0.40"
    airway_color = "#EF4444" if ri_calculada > 15.0 else ("#F59E0B" if ri_calculada > 10.0 else "#38BDF8")

    st.markdown(f"""
    <div class="panel-clinical">
        <div class="panel-header">MONITORIZACIÓN BIOMÉDICA DEL PACIENTE ACTIVO</div>
        <div style="font-size: 13px; font-family: monospace; line-height:1.4;">
            ID Paciente: <span class="data-highlight">{d['cama']}</span> | PCI Calculado: <span class="data-highlight">{pci} kg</span> | Diagnóstico Perfil: <span style="color:#F59E0B; font-weight:bold;">{", ".join(d['patologias'])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # REJILLA RESPONSIVA DOS COLUMNAS PRINCIPALES (PULMÓN IZQUIERDA / CÁLCULOS DERECHA)
    col_main1, col_main2 = st.columns([1, 1])
    
    with col_main1:
        st.markdown('<div class="panel-clinical"><div class="panel-header">ESTADO BIOLÓGICO DEL PARÉNQUIMA</div>', unsafe_allow_html=True)
        # Simulación Anatómica Vectorial de Alta Fidelidad
        st.markdown(f"""
        <div style="text-align: center; margin: 10px 0;">
            <svg width="280" height="230" viewBox="0 0 280 230" style="background:#090C14; border-radius:12px; border:1px solid #24324F;">
                <circle cx="140" cy="115" r="95" fill="{lung_color}" opacity="0.04" />
                <path d="M 140 15 L 140 65" stroke="{airway_color}" stroke-width="8" stroke-linecap="round" fill="none"/>
                <path d="M 140 65 Q 140 85 95 115" stroke="{airway_color}" stroke-width="6" stroke-linecap="round" fill="none"/>
                <path d="M 140 65 Q 140 85 185 115" stroke="{airway_color}" stroke-width="6" stroke-linecap="round" fill="none"/>
                <path d="M 130 75 C 100 55, 55 75, 55 135 C 55 180, 95 190, 120 170 C 125 165, 130 135, 130 75 Z" fill="{lung_color}" fill-opacity="{lung_opacity}" stroke="{stroke_glow}" stroke-width="2.5"/>
                <path d="M 150 75 C 180 55, 225 75, 225 135 C 225 180, 185 190, 160 170 C 155 165, 150 135, 150 75 Z" fill="{lung_color}" fill-opacity="{lung_opacity}" stroke="{stroke_glow}" stroke-width="2.5"/>
            </svg>
        </div>
        <div style="font-size:10px; font-family:monospace; color:{stroke_glow}; text-align:center; font-weight:bold; letter-spacing:0.2px;">{text_biomapa}</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_main2:
        st.markdown('<div class="panel-clinical"><div class="panel-header">DERIVACIONES COMPLEMENTARIAS</div>', unsafe_allow_html=True)
        
        # Lógica de colorimetría clínica para parámetros complementarios
        def color_val(val, g, y):
            if val >= g: return "#10B981" # Verde
            elif val >= y: return "#F59E0B" # Amarillo
            else: return "#EF4444" # Rojo
            
        def color_val_inv(val, y, r):
            if val <= y: return "#10B981" # Verde
            elif val <= r: return "#F59E0B" # Amarillo
            else: return "#EF4444" # Rojo

        c_stat_col = color_val(compliance_estatica, 40, 30)
        ri_col = color_val_inv(ri_calculada, 10, 15)
        mp_col = color_val_inv(mechanical_power, 12, 17)
        
        st.markdown(f"**Compliance Estática ($C_{{stat}}$):** <span style='color:{c_stat_col}; font-weight:bold;'>{compliance_estatica}</span> ml/cmH2O", unsafe_allow_html=True)
        st.markdown(f"**Elastancia Total del Sistema:** {elastancia_calculada} cmH2O/L")
        st.markdown(f"**Resistencia de Vía Aérea ($R_i$):** <span style='color:{ri_col}; font-weight:bold;'>{ri_calculada}</span> cmH2O/L/s", unsafe_allow_html=True)
        st.markdown(f"**Mechanical Power Acumulado:** <span style='color:{mp_col}; font-weight:bold;'>{mechanical_power}</span> J/min", unsafe_allow_html=True)
        
        # Color para índice de oxigenación (PAFI/SAFI)
        ox_col = "#10B981" if indice_ox > 300 else ("#F59E0B" if indice_ox > 200 else "#EF4444")
        metodo_label = 'PAFI' if 'Sí' in d['disp_gaso'] else 'SAFI'
        st.markdown(f"**Índice de Oxigenación ({metodo_label}):** <span style='color:{ox_col}; font-weight:bold;'>{indice_ox}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MÓDULOS REDISEÑADOS PREMIUM: MÉTRICAS DE SEGURIDAD (CON REPRESENTACIÓN ALVEOLAR CIRCULAR Y BALA DE O2) ---
    st.markdown('<div class="panel-clinical"><div class="panel-header">MÉTRICAS DE SEGURIDAD</div>', unsafe_allow_html=True)
    
    col_sec1, col_sec2, col_sec3 = st.columns(3)
    
    with col_sec1:
        st.markdown(f"<div class='security-metric-box'><span style='font-size:12px; font-weight:bold; color:#94A3B8;'>Volumen Corriente Relativo</span><br><span style='font-size:10px; color:#64748B;'>{vt_rango_texto}</span>", unsafe_allow_html=True)
        c_v_color = "#EF4444" if vt_relativo > max_vt else ("#F59E0B" if vt_relativo < min_vt else "#10B981")
        v_radius = min(42.0, max(15.0, 15.0 + ((vt_relativo - 4.0) * 6.5)))
        st.markdown(f"""
        <div style="text-align: center; margin: 12px 0;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="42" fill="none" stroke="#24324F" stroke-width="1.5" stroke-dasharray="3,3"/>
                <circle cx="50" cy="50" r="{v_radius}" fill="{c_v_color}" fill-opacity="0.3" stroke="{c_v_color}" stroke-width="3"/>
                <text x="50" y="54" text-anchor="middle" fill="#FFF" font-family="monospace" font-size="12" font-weight="bold">{vt_relativo}</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:11px; text-align:center; color:{c_v_color}; font-weight:bold;'>{ 'Sobrecarga' if vt_relativo > max_vt else ('Subóptimo' if vt_relativo < min_vt else 'Protector óptimo') }</div></div>", unsafe_allow_html=True)

    with col_sec2:
        st.markdown(f"<div class='security-metric-box'><span style='font-size:12px; font-weight:bold; color:#94A3B8;'>Driving Pressure (ΔP)</span><br><span style='font-size:10px; color:#64748B;'>(Normal: < 14.0 cmH2O)</span>", unsafe_allow_html=True)
        c_dp_color = "#EF4444" if driving_pressure >= 14.0 else ("#F59E0B" if driving_pressure >= 12.0 else "#10B981")
        dp_radius = min(42.0, max(15.0, 15.0 + ((driving_pressure - 5.0) * 2.2)))
        st.markdown(f"""
        <div style="text-align: center; margin: 12px 0;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="42" fill="none" stroke="#24324F" stroke-width="1.5" stroke-dasharray="3,3"/>
                <circle cx="50" cy="50" r="{dp_radius}" fill="{c_dp_color}" fill-opacity="0.3" stroke="{c_dp_color}" stroke-width="3"/>
                <text x="50" y="54" text-anchor="middle" fill="#FFF" font-family="monospace" font-size="12" font-weight="bold">{driving_pressure}</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:11px; text-align:center; color:{c_dp_color}; font-weight:bold;'>{ 'Estrés Crítico' if driving_pressure >= 14.0 else ('Zona Límite' if driving_pressure >= 12.0 else 'Seguro Parénquima') }</div></div>", unsafe_allow_html=True)

    with col_sec3:
        st.markdown(f"<div class='security-metric-box'><span style='font-size:12px; font-weight:bold; color:#94A3B8;'>Fracción Inspirada Oxígeno</span><br><span style='font-size:10px; color:#64748B;'>{fio2_rango_texto}</span>", unsafe_allow_html=True)
        c_f_color = "#EF4444" if float(d['fio2']) > max_fio2 else "#38BDF8"
        f_height = min(64.0, max(2.0, (float(d['fio2']) / 100.0) * 64.0))
        f_y = 77.0 - f_height
        st.markdown(f"""
        <div style="text-align: center; margin: 5px 0;">
            <svg width="100" height="107" viewBox="0 0 100 107">
                <path d="M 42 13 Q 50 2 58 13 Z" fill="none" stroke="#475569" stroke-width="2"/>
                <rect x="35" y="13" width="30" height="65" rx="6" ry="6" fill="none" stroke="#475569" stroke-width="2.5"/>
                <rect x="37" y="{f_y}" width="26" height="{f_height}" fill="{c_f_color}" fill-opacity="0.45"/>
                <text x="50" y="50" text-anchor="middle" fill="#FFF" font-family="monospace" font-size="11" font-weight="bold">{d['fio2']}%</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:11px; text-align:center; color:{c_f_color}; font-weight:bold;'>{ 'Toxicidad / Hiperoxia' if float(d['fio2']) > max_fio2 else 'Aporte Adecuado' }</div></div>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# PESTAÑA PROFESSIONAL PREMIUM: GASOMETRÍA
# -----------------------------------------------------------------------------------------
elif chosen_tab == "Gasometría":
    st.markdown('<div class="panel-clinical"><div class="panel-header">ANÁLISIS COMPLETO DEL EQUILIBRIO ÁCIDO-BASE</div>', unsafe_allow_html=True)
    col_layout1, col_layout2 = st.columns([1, 1])
    with col_layout1:
        st.markdown("<div class='section-title-sub'>1. Contexto y Perfil de Línea Base</div>", unsafe_allow_html=True)
        g_antecedente = st.selectbox("Antecedentes Personales:", ["Ninguno / Agudo puro", "EPOC / Obeso (Retenedor crónico)", "Insuficiencia renal crónica"], label_visibility="collapsed")
    with col_layout2: st.markdown("<div class='section-title-sub'>2. Parámetros del Analizador de Gases</div>", unsafe_allow_html=True)
        
    col_num1, col_num2, col_num3, col_num4 = st.columns(4)
    with col_num1: g_ph = st.number_input("pH", min_value=6.80, max_value=7.80, value=7.40, step=0.01)
    with col_num2: g_pco2 = st.number_input("pCO2 (mmHg)", min_value=10.0, max_value=150.0, value=40.0, step=1.0)
    with col_num3: g_hco3 = st.number_input("HCO3- (mEq/L)", min_value=5.0, max_value=60.0, value=24.0, step=1.0)
    with col_num4: g_po2 = st.number_input("pO2 Arterial (mmHg)", min_value=20.0, max_value=500.0, value=90.0, step=1.0)
        
    diagnostico_final = "NORMAL / EQUILIBRIO FISIOLÓGICO BASAL"
    bg_color, border_color, text_color = "rgba(16, 185, 129, 0.15)", "#10B981", "#A7F3D0"
    directrices_clinicas = "Todos los valores analizados se encuentran dentro del rango adaptativo estándar."
    
    pco2_base, hco3_base = 40.0, 24.0
    if g_antecedente == "EPOC / Obeso (Retenedor crónico)": pco2_base, hco3_base = 48.0, 29.0
    elif g_antecedente == "Insuficiencia renal crónica": hco3_base = 20.0

    if g_ph < 7.35:  # ACIDEMIA
        if g_pco2 > pco2_base and g_hco3 < hco3_base:
            diagnostico_final = "ACIDOSIS MIXTA SEVERA CRÍTICA"
            bg_color, border_color, text_color = "rgba(239, 68, 68, 0.18)", "#EF4444", "#FCA5A5"
            directrices_clinicas = "Fallo multiorgánico o parada inminente. Aumente la ventilación minuto de forma urgente y optimice la perfusión tisular sistémica."
        elif g_pco2 > pco2_base:
            if g_antecedente == "EPOC / Obeso (Retenedor crónico)":
                hco3_esperado = hco3_base + (0.35 * (g_pco2 - pco2_base))
                if g_hco3 < hco3_esperado - 2:
                    diagnostico_final = "ACIDOSIS RESPIRATORIA CRÓNICA AGUDIZADA CON ACIDOSIS METABÓLICA CONCOMITANTE"
                    bg_color, border_color, text_color = "rgba(239, 68, 68, 0.15)", "#EF4444", "#FCA5A5"
                else:
                    diagnostico_final = "ACIDOSIS RESPIRATORIA CRÓNICA REGULADA COMPENSADA"
                    bg_color, border_color, text_color = "rgba(16, 185, 129, 0.15)", "#10B981", "#A7F3D0"
            else:
                hco3_esperado = hco3_base + (0.1 * (g_pco2 - pco2_base))
                diagnostico_final = "ACIDOSIS RESPIRATORIA AGUDA DESCOMPENSADA" if g_hco3 < hco3_esperado - 2 else "ACIDOSIS RESPIRATORIA AGUDA PURA"
                bg_color, border_color, text_color = "rgba(245, 158, 11, 0.15)", "#F59E0B", "#FDE68A"
            directrices_clinicas = "Retención de CO2. Ajustar frecuencia o volumen corriente en el respirador vigilando estrechamente la Driving Pressure."
        elif g_hco3 < hco3_base:
            pco2_esperada = (1.5 * g_hco3) + 8.0
            diagnostico_final = "ACIDOSIS METABÓLICA CON ACIDOSIS RESPIRATORIA ASOCIADA (Fatiga diafragmática)" if g_pco2 > pco2_esperada + 2 else "ACIDOSIS METABÓLICA PURA UNIDIRECCIONAL"
            bg_color, border_color, text_color = "rgba(239, 68, 68, 0.15)", "#EF4444", "#FCA5A5"
            directrices_clinicas = "Consumo de bicarbonato plasmático. Descarte hipoperfusión tisular midiendo el Lactato central."

    elif g_ph > 7.45:  # ALCALEMIA
        if g_pco2 < pco2_base and g_hco3 > hco3_base:
            diagnostico_final = "ALCALOSIS MIXTA GRAVE"
            bg_color, border_color, text_color = "rgba(239, 68, 68, 0.15)", "#EF4444", "#FCA5A5"
        elif g_pco2 < pco2_base:
            diagnostico_final = "ALCALOSIS RESPIRATORIA PURA (Hiperventilación)"
            bg_color, border_color, text_color = "rgba(245, 158, 11, 0.15)", "#F59E0B", "#FDE68A"
            directrices_clinicas = "Lavado excesivo de CO2. Controle dolor, sedación, fiebre o asincronías con el ventilador."
        elif g_hco3 > hco3_base:
            pco2_esperada = (0.7 * g_hco3) + 21.0
            diagnostico_final = "ALCALOSIS METABÓLICA CON ACIDOSIS RESPIRATORIA SOBREAÑADIDA" if g_pco2 > pco2_esperada + 2 else "ALCALOSIS METABÓLICA PURA COMPENSADA"
            bg_color, border_color, text_color = "rgba(16, 185, 129, 0.15)", "#10B981", "#A7F3D0"

    st.markdown("<div class='section-title-sub' style='margin-top:15px;'>3. Dictamen Fisiológico Automatizado</div>", unsafe_allow_html=True)
    st.markdown(f'<div class="gaso-alert-card" style="background: {bg_color}; border: 1px solid {border_color}; color: {text_color};">{diagnostico_final}</div>', unsafe_allow_html=True)
    
    pointer_position = ((max(6.80, min(7.80, g_ph)) - 6.80) / (7.80 - 6.80)) * 100
    st.markdown(f'<div class="ph-gauge-bg"><div class="ph-gauge-pointer" style="left: calc({pointer_position}% - 3px);"></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 12px; color: #94A3B8; border: 1px dashed #24324F; padding: 12px; border-radius: 8px; background:#0B0F19;"><b>Directrices de Soporte Clínico:</b> {directrices_clinicas}</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color:#24324F; margin: 15px 0;'>", unsafe_allow_html=True)
    if g_po2 < 60.0: st.markdown("<div class='risk-box' style='background-color: rgba(239, 68, 68, 0.15); color: #FCA5A5; border: 1px solid #EF4444;'>INSUFICIENCIA RESPIRATORIA AGUDA CRÍTICA (PaO2 < 60 mmHg)</div>", unsafe_allow_html=True)
    else: st.markdown("<div class='risk-box' style='background-color: rgba(16, 185, 129, 0.15); color: #A7F3D0; border: 1px solid #10B981;'>OXIGENACIÓN EN RANGO FISIOLÓGICO SEGURO</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# PESTAÑA: ACADEMIA
# -----------------------------------------------------------------------------------------
elif chosen_tab == "Academia":
    st.markdown('<div class="panel-clinical"><div class="panel-header">ENCICLOPEDIA CIENTÍFICA</div>', unsafe_allow_html=True)
    tab_aca1, tab_aca2, tab_aca3, tab_aca4 = st.tabs(["Fisiología", "Patrones", "Fisiopatología", "Weaning"])
    with tab_aca1:
        st.markdown("### Monitorización y Derivaciones Avanzadas")
        with st.expander("Driving Pressure (ΔP)"):
            st.markdown("<div class='academic-text'>Gradiente elástico alveolar neto: $\Delta P = P_{\text{pausa}} - \text{PEEP}_{\text{total}}$. Valores $\ge 14\text{ cmH2O}$ incrementan el estrés estructural del parénquima.</div>", unsafe_allow_html=True)
        with st.expander("Mechanical Power y Resistencia (Ri)"):
            st.markdown("<div class='academic-text'><b>Mechanical Power:</b> Energía transmitida al parénquima por minuto. Límite: <b>17 J/min</b>.<br><b>Resistencia Inspiratoria ($R_i$):</b> Mide la fricción bronquial:<br>$$R_i = \\frac{P_{\text{pico}} - P_{\text{pausa}}}{\\text{Flujo (L/s)}}$$</div>", unsafe_allow_html=True)
    with tab_aca2:
        st.markdown("### Clasificación por Patrones Biofísicos")
        st.markdown("<div class='academic-subtitle'>Patrón Obstructivo (Problema de Tubería)</div>", unsafe_allow_html=True)
        st.markdown("<div class='academic-text'>Fricción elevada por broncoespasmo o moco ($R_e$ alta). Provoca atrapamiento aéreo y Auto-PEEP. Exige tiempos de espiración largos (I:E 1:3 o 1:4).</div>", unsafe_allow_html=True)
        st.markdown("<div class='academic-subtitle'>Patrón Restrictivo (Problema de Globo Rígido)</div>", unsafe_allow_html=True)
        st.markdown("<div class='academic-text'>Pérdida drástica de compliance ($C_{stat} < 30\text{ ml/cmH2O}$) por exudado (SDRA). Requiere volúmenes bajos de 4-6 ml/kg y PEEP protectora para evitar colapso cíclico.</div>", unsafe_allow_html=True)
    with tab_aca3:
        st.markdown("### Patologías Comunes")
        with st.expander("SDRA de Berlín e Hiperoxia en EPOC"):
            st.markdown("<div class='academic-text'><b>Berlín SDRA:</b> Estratificación por PAFI: Leve (200-300), Moderado (100-200), Severo (<100 mmHg).<br><b>EPOC:</b> FiO2 >40% anula la vasoconstricción hipóxica adaptativa, eleva el espacio muerto y causa narcosis hipercápnica por efecto Haldane. Meta: 88-92%.</div>", unsafe_allow_html=True)
    with tab_aca4:
        st.markdown("### Fisiología Aplicada al Weaning")
        with st.expander("P0.1 e Índice ROX"):
            st.markdown("<div class='academic-text'><b>P0.1 Maquet:</b> Drive central bulbar en los primeros 100ms ocluyendo de forma silente la válvula. Rango óptimo: 1.5 a 3.5 cmH2O.<br><b>Índice ROX:</b> Retirada a CNAF. Un valor <b><4.88</b> predice fallo neuromuscular del alto flujo exigiendo reevaluar intubación.</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------
# PESTAÑA: DATA
# -----------------------------------------------------------------------------------------
elif chosen_tab == "Data":
    st.markdown('<div class="panel-clinical"><div class="panel-header">REGISTRO CIENTÍFICO ACUMULATIVO DE LA UNIDAD</div>', unsafe_allow_html=True)
    if st.session_state.db.empty:
        st.info("La base de datos local de la sesión está vacía. Registre datos desde la pestaña 'Valores'.")
    else:
        st.markdown("<div class='section-title-sub'>Historial Evolutivo y Gráficos de Tendencias</div>", unsafe_allow_html=True)
        lista_pacientes = st.session_state.db['Paciente_ID'].unique()
        paciente_sel = st.selectbox("Buscar por ID de Paciente:", lista_pacientes, index=list(lista_pacientes).index(d['cama']) if d['cama'] in lista_pacientes else 0)
        df_paciente = st.session_state.db[st.session_state.db['Paciente_ID'] == paciente_sel].copy().sort_values(by='Fecha_Hora')
        
        opciones_metricas = {
            'Driving_Pressure_cmH2O': 'Driving Pressure (ΔP)', 'Compliance_Estatica_ml_cmH2O': 'Compliance Estática (Cstat)', 'FiO2_Porcentaje': 'Fracción de Oxígeno (FiO2)', 'Parametro_Volumen_ml': 'Volumen Tidal (Vt)', 'Presion_Pico_cmH2O': 'Presion Pico (Ppico)', 'Auto_PEEP_cmH2O': 'Auto-PEEP', 'Mechanical_Power_J_min': 'Mechanical Power', 'Indice_Oxigenacion_Calculado': 'Índice de Oxigenación', 'Tobin_RSBI': 'Índice de Tobin (RSBI)', 'Rox_Indice': 'Índice ROX'
        }
        metricas_seleccionadas = st.multiselect("Selecciona los parámetros para la curva temporal:", options=list(opciones_metricas.keys()), format_func=lambda x: opciones_metricas[x], default=['Driving_Pressure_cmH2O', 'Compliance_Estatica_ml_cmH2O'])
        
        if metricas_seleccionadas:
            st.line_chart(df_paciente.set_index('Fecha_Hora')[metricas_seleccionadas], use_container_width=True)
            
        st.markdown("<br><hr style='border-color:#24324F; margin:10px 0;'><br>", unsafe_allow_html=True)
        st.dataframe(df_paciente, use_container_width=True)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.db.to_excel(writer, index=False, sheet_name='Data_Ventcheck')
        st.download_button(label="DESCARGAR DATASET EN FORMATO EXCEL (.XLSX)", data=output.getvalue(), file_name=f"Ventcheck_Data_{datetime.date.today().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
