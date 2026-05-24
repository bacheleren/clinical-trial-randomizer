# Clinical Trial Randomizer 🏥 / Randomizador de Ensaios Clínicos 

*🌍 [Click here for the English version](#english-version) | 🇧🇷 [Clique aqui para a versão em Português](#versão-em-português)*

---

## English Version

A lightweight, deterministic, and stateless clinical trial randomizer built with Python and Streamlit. 

This application provides a scientifically rigorous randomization process without the overhead of backend databases or complex user authentication. It is designed to prioritize clinical usability, rapid allocation, and clear source documentation while maintaining mathematical reproducibility.

### Key Features

* **Deterministic Seed Logic:** Combines a user-defined Study Seed and Sample Size to generate a mathematically reproducible allocation list. 
* **Randomly Permuted Blocks:** Utilizes random block sizes of 2, 4, and 6 to ensure group balancing while preventing allocation prediction (selection bias).
* **URL Parameter Configuration:** Admins configure the study once and generate a custom URL. When clinicians open the link, the app is pre-configured and in their native language.
* **Stateless Architecture:** No backend database is required. Clinicians input the Sequence Number, eliminating the risk of accidental double-clicks ruining a locked sequence.
* **Audit-Ready Outputs:** Accepts an optional Subject ID purely for cosmetic output, allowing clinicians to take a clear screenshot for source data verification.
* **Admin Troubleshooting View:** An expandable view behind a safety warning allows study administrators to view the master list for auditing.

### How to Use

#### 1. Admin Setup (Lead Investigator / Statistician)
1. Open the application.
2. Select your desired language in the sidebar (English 🇺🇸 or Português 🇧🇷).
3. Enter the **Study Seed** (e.g., `studyname`) and the **Sample Size** (e.g., `140`).
4. The application will immediately generate a full, shareable URL (e.g., `https://clinical-trial-randomizer.streamlit.app/?seed=studyname&size=140&lang=en`).
5. Distribute this exact link to the clinical sites.
6. *Optional:* Expand the "Troubleshooting" tab and click the red alert button to safely view the master list.

#### 2. Clinician Workflow (Enrolling a Patient)
1. Open the custom URL provided by the study admin.
2. Enter the **Patient Sequence Number** (e.g., patient number 13).
3. Enter the **Subject ID / Initials** (e.g., ABC-103).
4. Click **Generate Allocation**.
5. Record the output in the patient's source documentation.

---

## Versão em Português

Um randomizador para ensaios clínicos leve, determinístico e "stateless" (sem armazenamento de estado), construído com Python e Streamlit.

Este aplicativo fornece um processo de randomização rigoroso, sem a necessidade de manter bancos de dados complexos ou sistemas de autenticação. Foi projetado priorizando a usabilidade clínica, alocação rápida e documentação clara, mantendo a reprodutibilidade matemática.

### Principais Funcionalidades

* **Lógica de Seed Determinística:** Combina uma seed definida pelo usuário e o Tamanho da Amostra para gerar uma lista de alocação matematicamente reprodutível.
* **Blocos Aleatórios Permutados:** Utiliza blocos de tamanhos aleatórios (2, 4 e 6) para garantir o balanceamento e evitar a previsão de alocação (viés de seleção).
* **Configuração por Parâmetros de URL:** Administradores configuram o estudo uma vez e geram uma URL customizada. Quando os clínicos abrem o link, o app já está configurado no idioma correto.
* **Arquitetura Stateless:** Não requer banco de dados. Os clínicos inserem o Número de Sequência exato, eliminando o risco de cliques duplos acidentais arruinarem uma sequência.
* **Saídas Prontas para Auditoria:** Aceita ID do Sujeito opcionalmente para permitir que os clínicos tirem prints (capturas de tela) com a identificação do paciente para verificação.
* **Visualização para Auditoria (Admin):** Uma visão protegida por um aviso de segurança permite que administradores visualizem a lista principal.

### Como Usar

#### 1. Configuração do Administrador (Investigador Principal / Estatístico)
1. Abra o aplicativo.
2. Selecione o idioma desejado na barra lateral (English 🇺🇸 ou Português 🇧🇷).
3. Insira a **Seed do Estudo** (ex: `nome-do-estudo`) e o **Tamanho da Amostra** (ex: `140`).
4. O aplicativo gerará imediatamente uma URL de compartilhamento (ex: `https://clinical-trial-randomizer.streamlit.app/?seed=nome-do-estudo&size=140&lang=pt`).
5. Distribua este link exato para os centros de pesquisa.
6. *Opcional:* Expanda a aba "Solução de Problemas" e clique no botão de alerta vermelho para visualizar a lista principal com segurança.

#### 2. Fluxo de Trabalho do Clínico (Inclusão de Paciente)
1. Abra a URL customizada fornecida pelo administrador.
2. Insira o **Número de Sequência do Paciente** (ex: 13).
3. Insira o **ID do Sujeito / Iniciais** (ex: ABC-103).
4. Clique em **Gerar Alocação**.
5. Registre o resultado nos documentos fonte do paciente.

---

### Deployment / Implantação
Designed for easy deployment via [Streamlit Community Cloud](https://share.streamlit.io/).
Requires: `streamlit`, `pandas`

### License / Licença
MIT License. Provided "as-is" for the scientific and clinical community.

*Developed by Guilherme Bächtold.*
