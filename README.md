# Clinical Trial Randomizer 🏥

A lightweight, deterministic, and stateless clinical trial randomizer built with Python and Streamlit. 

This application provides a scientifically rigorous randomization process without the overhead of backend databases or complex user authentication. It is designed to prioritize clinical usability, rapid allocation, and clear source documentation while maintaining mathematical reproducibility.

Try it now: [Working Streamlit App](https://clinical-trial-randomizer.streamlit.app/)

## Key Features

* **Deterministic Seed Logic:** Combines a user-defined Study Seed and Sample Size to generate a mathematically reproducible allocation list. The same inputs will always yield the exact same master list.
* **Randomly Permuted Blocks:** Utilizes random block sizes of 2, 4, and 6 to ensure group balancing while preventing allocation prediction (selection bias) by clinical staff.
* **URL Parameter Configuration:** Admins can configure the study once and generate a custom URL. When clinicians open the link, the randomizer is pre-configured and ready to use.
* **Stateless Architecture:** No backend database is required. Clinicians input the exact Sequence Number for the patient in front of them. This "stateless" approach eliminates the risk of accidental double-clicks or test entries ruining a locked sequence.
* **Audit-Ready Outputs:** Accepts an optional "Subject ID / Initials" purely for cosmetic output, allowing clinicians to take a screenshot or print the assignment with the specific patient's identifier clearly visible for source data verification.
* **Admin Troubleshooting View:** A segregated, expandable view allows study administrators or statisticians to view the complete master list for auditing or end-of-study reconciliation.

## How to Use

### 1. Admin Setup (Lead Investigator / Statistician)
1. Open the application.
2. In the left sidebar, enter the **Study Seed** (e.g., `mystudy2026`) and the **Sample Size** (e.g., `140`).
3. The application will immediately generate a shareable URL parameter string (e.g., `/?seed=mystudy2026&size=140`).
4. Append this string to your Streamlit app's base URL and distribute this link to the clinical sites.
5. *Optional:* Expand the "Troubleshooting" tab in the sidebar to view or export the full master randomization list.

### 2. Clinician Workflow (Enrolling a Patient)
1. Open the custom URL provided by the study admin.
2. Enter the **Patient Sequence Number** (e.g., patient number 13).
3. Enter the **Subject ID / Initials** (e.g., ABC-103) for your records.
4. Click **Generate Allocation**.
5. Record the output (e.g., "Enrollment #13 (ABC-103) Assigned to: Group 2") in the patient's source documentation.

## Deployment Instructions

This app is optimized for deployment on Streamlit Community Cloud.

1. Upload `randomizer.py` and `requirements.txt` to a GitHub repository.
2. Navigate to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub account and select the repository.
4. Click **Deploy**. The app will be live and accessible via a public link in minutes.

## Requirements
* `streamlit`
* `pandas`
