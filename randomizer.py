import streamlit as st
import random
import pandas as pd

# --- CORE ALGORITHM ---
def generate_randomization_list(seed_text, sample_size):
    # Combine the seed word and sample size to create a unique, reproducible state
    combined_seed = f"{seed_text}_{sample_size}"
    random.seed(combined_seed)
    
    groups = ["Group 1", "Group 2"]
    block_sizes = [2, 4, 6]
    
    randomization_list = []
    
    # Generate random blocks until we hit the required sample size
    while len(randomization_list) < sample_size:
        current_block_size = random.choice(block_sizes)
        
        # Split the block equally between Group 1 and Group 2
        half_size = current_block_size // 2
        block = (groups[:1] * half_size) + (groups[1:] * half_size)
        
        # Shuffle this specific block deterministically based on the seed
        random.shuffle(block)
        
        randomization_list.extend(block)
        
    # Truncate the list to the exact sample size requested
    return randomization_list[:sample_size]


# --- STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="Clinical Trial Randomizer", page_icon="🏥")

# 1. Read URL Parameters (for easy sharing)
query_params = st.query_params
url_seed = query_params.get("seed", "")
url_size = query_params.get("size", "140") 

# 2. Sidebar: Admin & Setup
with st.sidebar:
    st.header("⚙️ Study Setup")
    st.write("Configure the trial parameters here.")
    
    active_seed = st.text_input("Study Seed (e.g., studyname)", value=url_seed)
    active_size = st.number_input("Sample Size", min_value=1, value=int(url_size) if url_size.isdigit() else 140)
    
    if active_seed:
        st.success("Study configured.")
        st.write("**Shareable URL:**")
        # Generates the full, direct URL for the clinical staff
        full_url = f"https://clinical-trial-randomizer.streamlit.app/?seed={active_seed}&size={active_size}"
        st.code(full_url)
        
    st.divider()
    
    with st.expander("Troubleshooting: View Master List"):
        st.warning("⚠️ For Statistician/Auditing use only. Do not use for patient allocation. Viewing this list breaks allocation concealment.")
        if active_seed:
            # Added safety feature: explicit red button click required to reveal the list
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
    st.info("👈 Please enter a Study Seed in the sidebar to begin, or use a pre-configured study link.")
else:
    st.markdown("Enter the patient details below to generate their group assignment.")
    
    col1, col2 = st.columns(2)
    with col1:
        patient_no = st.number_input("Patient Sequence Number", min_value=1, max_value=active_size, step=1)
    with col2:
        patient_id = st.text_input("Subject ID / Initials (Optional)")
        
    # Changed to secondary button so the red warning button stands out more in the sidebar
    if st.button("Generate Allocation"):
        # Generate the list silently in the background
        master_list = generate_randomization_list(active_seed, active_size)
        
        # Find the specific patient's allocation (List index is Patient No. - 1)
        allocation = master_list[patient_no - 1]
        
        st.divider()
        
        # Display the result formatted for source documentation screenshotting
        if patient_id:
            st.success(f"### Enrollment #{patient_no} ({patient_id}) \n## Assigned to: **{allocation}**")
        else:
            st.success(f"### Enrollment #{patient_no} \n## Assigned to: **{allocation}**")
            
        st.caption("Please record this assignment in the patient's source documentation.")

# 4. Documentation & Addendum
st.markdown("<br><br>", unsafe_allow_html=True)
st.info(
    "**Instructions & Documentation**\n\n"
    "For full usage instructions, methodological details, or to offer suggestions, please visit the "
    "[GitHub Repository](https://github.com/bacheleren/clinical-trial-randomizer)."
)

# 5. Footer
st.divider()
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.85em;'>"
    "Developed by Guilherme Bächtold | "
    "<a href='https://github.com/bacheleren/clinical-trial-randomizer' target='_blank' style='color: gray; text-decoration: underline;'>View Source</a>"
    "</p>", 
    unsafe_allow_html=True
)
