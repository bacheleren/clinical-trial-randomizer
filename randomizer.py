import streamlit as st
import random
import pandas as pd

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

# 1. Read URL Parameters & Initialize State
query_params = st.query_params
url_seed = query_params.get("seed", "")
url_size = query_params.get("size", "140") 

# Use session state to lock in variables after button press or URL load
if "study_seed" not in st.session_state:
    st.session_state.study_seed = url_seed
if "study_size" not in st.session_state:
    st.session_state.study_size = int(url_size) if url_size.isdigit() else 140

# 2. Sidebar: Admin & Setup
with st.sidebar:
    st.header("⚙️ Study Setup")
    st.write("Configure the trial parameters here.")
    
    # Wrap inputs in a form so they only update upon clicking the button
    with st.form("setup_form"):
        input_seed = st.text_input("Study Seed (e.g., studyname)", value=st.session_state.study_seed)
        input_size = st.number_input("Sample Size", min_value=1, value=st.session_state.study_size)
        
        # Mobile-friendly submission button
        submitted = st.form_submit_button("Configure Study", type="primary")
        
        if submitted:
            st.session_state.study_seed = input_seed
            st.session_state.study_size = input_size

    # Assign active variables from locked-in state
    active_seed = st.session_state.study_seed
    active_size = st.session_state.study_size
    
    if active_seed:
        st.success("Study configured.")
        st.write("**Shareable URL:**")
        full_url = f"https://clinical-trial-randomizer.streamlit.app/?seed={active_seed}&size={active_size}"
        st.code(full_url)
        
        st.divider()
        
        with st.expander("Troubleshooting: View Master List"):
            st.warning("⚠️ For Statistician/Auditing use only. Do not use for patient allocation. Viewing this list breaks allocation concealment.")
            if st.button("🚨 REVEAL MASTER LIST 🚨", type="primary"):
                full_list = generate_randomization_list(active_seed, active_size)
                df = pd.DataFrame({
                    "Enrollment No.": range(1, active_size + 1), 
                    "Allocation": full_list
                })
                st.dataframe(df, hide_index=True)

# 3. Main Page: Clinician Interface
st.title("Patient Randomization")

if not active_seed:
    st.info("👈 Please enter a Study Seed and click 'Configure Study' in the sidebar to begin, or use a pre-configured study link.")
else:
    st.markdown("Enter the patient details below to generate their group assignment.")
    
    col1, col2 = st.columns(2)
    with col1:
        patient_no = st.number_input("Patient Sequence Number", min_value=1, max_value=active_size, step=1)
    with col2:
        patient_id = st.text_input("Subject ID / Initials (Optional)")
        
    if st.button("Generate Allocation"):
        master_list = generate_randomization_list(active_seed, active_size)
        allocation = master_list[patient_no - 1]
        
        st.divider()
        
        if patient_id:
            st.success(f"### Enrollment #{patient_no} ({patient_id}) \n## Assigned to: **{allocation}**")
        else:
            st.success(f"### Enrollment #{patient_no} \n## Assigned to: **{allocation}**")
            
        st.caption("Please record this assignment in the patient's source documentation.")

# 4. Sticky Footer with CSS
footer_css = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: gray;
    text-align: center;
    font-size: 0.85em;
    padding: 10px 0;
    z-index: 100;
}
</style>
<div class="footer">Developed by Guilherme Bächtold</div>
"""
st.markdown(footer_css, unsafe_allow_html=True)
