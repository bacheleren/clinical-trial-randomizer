import streamlit as st
import random
import pandas as pd

# --- TRANSLATION DICTIONARY ---
t = {
    "en": {
        "page_title": "Patient Randomization",
        "setup_title": "⚙️ Study Setup",
        "setup_desc": "Configure the trial parameters here.",
        "seed_label": "Study Seed (e.g., studyname)",
        "size_label": "Sample Size",
        "lang_label": "App Language",
        "configured": "Study configured.",
        "url_label": "**Shareable URL:**",
        "troubleshoot": "Troubleshooting: View Master List",
        "warning": "⚠️ For Statistician/Auditing use only. Do not use for patient allocation. Viewing this list breaks allocation concealment.",
        "reveal_btn": "🚨 REVEAL MASTER LIST 🚨",
        "info_start": "👈 Please enter a Study Seed in the sidebar to begin, or use a pre-configured study link.",
        "instruction": "Enter the patient details below to generate their group assignment.",
        "seq_label": "Patient Sequence Number",
        "id_label": "Subject ID / Initials (Optional)",
        "gen_btn": "Generate Allocation",
        "enrollment": "Enrollment",
        "assigned": "Assigned to",
        "record_caption": "Please record this assignment in the patient's source documentation.",
        "docs": "**Instructions & Documentation**\n\nFor full usage instructions, methodological details, or to offer suggestions, please visit the [GitHub Repository](https://github.com/bacheleren/clinical-trial-randomizer).",
        "footer": "Developed by Guilherme Bächtold | <a href='https://github.com/bacheleren/clinical-trial-randomizer' target='_blank' style='color: gray; text-decoration: underline;'>View Source</a>"
    },
    "pt": {
        "page_title": "Randomização de Pacientes",
        "setup_title": "⚙️ Configuração do Estudo",
        "setup_desc": "Configure os parâmetros do estudo aqui.",
        "seed_label": "Semente do Estudo (ex: nome-do-estudo)",
        "size_label": "Tamanho da Amostra",
        "lang_label": "Idioma do App",
        "configured": "Estudo configurado.",
        "url_label": "**URL de Compartilhamento:**",
        "troubleshoot": "Solução de Problemas: Ver Lista Principal",
        "warning": "⚠️ Apenas para uso do Estatístico/Auditor. Não utilize para alocação de pacientes. Visualizar esta lista quebra o sigilo de alocação.",
        "reveal_btn": "🚨 REVELAR LISTA PRINCIPAL 🚨",
        "info_start": "👈 Por favor, insira a Semente do Estudo na barra lateral para começar, ou use um link pré-configurado.",
        "instruction": "Insira os detalhes do paciente abaixo para gerar sua alocação de grupo.",
        "seq_label": "Número de Sequência do Paciente",
        "id_label": "ID do Sujeito / Iniciais (Opcional)",
        "gen_btn": "Gerar Alocação",
        "enrollment": "Inclusão",
        "assigned": "Alocado para",
        "record_caption": "Por favor, registre esta alocação nos documentos fonte do paciente.",
        "docs": "**Instruções e Documentação**\n\nPara instruções completas de uso, detalhes metodológicos ou para oferecer sugestões, visite o [Repositório do GitHub](https://github.com/bacheleren/clinical-trial-randomizer).",
        "footer": "Desenvolvido por Guilherme Bächtold | <a href='https://github.com/bacheleren/clinical-trial-randomizer' target='_blank' style='color: gray; text-decoration: underline;'>Ver Código Fonte</a>"
    }
}

# --- CORE ALGORITHM ---
def generate_randomization_list(seed_text, sample_size):
    combined_seed = f"{seed_text}_{sample_size}"
    random.seed(combined_seed)
    
    groups = ["Group 1", "Group 2"]
    block_sizes = [2, 4, 6]
    randomization_list = []
    
    while len(randomization_list) < sample_size:
        current_block_size = random.choice(block_sizes)
        half_size = current_block_size // 2
        block = (groups[:1] * half_size) + (groups[1:] * half_size)
        random.shuffle(block)
        randomization_list.extend(block)
        
    return randomization_list[:sample_size]

# --- STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="Clinical Trial Randomizer", page_icon="🏥")

# 1. Read URL Parameters
query_params = st.query_params
url_seed = query_params.get("seed", "")
url_size = query_params.get("size", "140")
url_lang = query_params.get("lang", "en")

# Ensure language is valid, default to English
if url_lang not in ["en", "pt"]:
    url_lang = "en"

# Map internal lang codes to UI display options
lang_options = {"en": "English 🇺🇸", "pt": "Português 🇧🇷"}
reverse_lang_options = {v: k for k, v in lang_options.items()}

# 2. Sidebar: Admin & Setup
with st.sidebar:
    # First get the language choice so the rest of the UI can translate instantly
    selected_display_lang = st.radio("Language / Idioma", options=list(lang_options.values()), index=0 if url_lang == "en" else 1)
    lang = reverse_lang_options[selected_display_lang]
    
    st.divider()
    st.header(t[lang]["setup_title"])
    st.write(t[lang]["setup_desc"])
    
    active_seed = st.text_input(t[lang]["seed_label"], value=url_seed)
    active_size = st.number_input(t[lang]["size_label"], min_value=1, value=int(url_size) if url_size.isdigit() else 140)
    
    if active_seed:
        st.success(t[lang]["configured"])
        st.write(t[lang]["url_label"])
        # Generate the full URL including the selected language parameter
        full_url = f"https://clinical-trial-randomizer.streamlit.app/?seed={active_seed}&size={active_size}&lang={lang}"
        st.code(full_url)
        
    st.divider()
    
    with st.expander(t[lang]["troubleshoot"]):
        st.warning(t[lang]["warning"])
        if active_seed:
            if st.button(t[lang]["reveal_btn"], type="primary"):
                full_list = generate_randomization_list(active_seed, active_size)
                df = pd.DataFrame({
                    "Enrollment No.": range(1, active_size + 1), 
                    "Allocation": full_list
                })
                st.dataframe(df, hide_index=True)

# 3. Main Page: Clinician Interface
st.title(t[lang]["page_title"])

if not active_seed:
    st.info(t[lang]["info_start"])
else:
    st.markdown(t[lang]["instruction"])
    
    col1, col2 = st.columns(2)
    with col1:
        patient_no = st.number_input(t[lang]["seq_label"], min_value=1, max_value=active_size, step=1)
    with col2:
        patient_id = st.text_input(t[lang]["id_label"])
        
    if st.button(t[lang]["gen_btn"]):
        master_list = generate_randomization_list(active_seed, active_size)
        allocation = master_list[patient_no - 1]
        
        st.divider()
        
        if patient_id:
            st.success(f"### {t[lang]['enrollment']} #{patient_no} ({patient_id}) \n## {t[lang]['assigned']}: **{allocation}**")
        else:
            st.success(f"### {t[lang]['enrollment']} #{patient_no} \n## {t[lang]['assigned']}: **{allocation}**")
            
        st.caption(t[lang]["record_caption"])

# 4. Documentation & Addendum
st.markdown("<br><br>", unsafe_allow_html=True)
st.info(t[lang]["docs"])

# 5. Footer
st.divider()
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 0.85em;'>{t[lang]['footer']}</p>", 
    unsafe_allow_html=True
)
