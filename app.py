import os
import tempfile
import zipfile
import streamlit as st

# Safe cross-platform folder picker defined internally
# (Prevents missing function errors in repository_scanner.py)
def safe_open_folder_dialog():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory()
        root.destroy()
        return folder_selected if folder_selected else None
    except Exception:
        return None

# Import repository_scanner safely
try:
    from repository_scanner import scan_repository
except ImportError:
    from scanners.source_scanner import scan_repository

from mosca_engine import calculate_mosca_risk
from pqc_recommendations import get_pqc_recommendations
from cbom_formatter import generate_cbom

# Streamlit Page Configuration
st.set_page_config(
    page_title="ECDAT - Cryptographic Discovery & Quantum Readiness",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Unified Cryptographic Asset Inventory & Quantum Readiness")

# Sidebar Configuration
st.sidebar.header("Risk Calculation & Scenario Settings")
risk_technique = st.sidebar.radio(
    "Select Assessment Technique:",
    [
        "Standard Mosca Inequality (X + Y > Z)",
        "Sensitivity-Weighted QPS (W × max(1, (X+Y)/Z))",
        "Data Shelf-Life Ratio (X / Z)"
    ]
)

st.sidebar.header("CRQC Horizon Assumption (Z)")
z_horizon = st.sidebar.slider(
    "Assumed Years until CRQC Arrival (Z):",
    min_value=1,
    max_value=30,
    value=10
)

st.sidebar.header("Global Environment & Defaults Override")
env = st.sidebar.selectbox(
    "Default Deployment Environment:",
    ["Production", "Staging", "Development"]
)
enable_pqc_sim = st.sidebar.checkbox("Enable PQC Migration Simulation Mode", value=False)

# Discovery Source Header
st.subheader("Discovery Source — Source Code Repository")
st.write(
    "Scan a local source-code repository folder or upload a ZIP. "
    "ECDAT recursively discovers source files, scans them for cryptographic artefacts, "
    "and sends the findings through the same risk, Mosca, and recommendation engines."
)

# Repository Input Toggle
input_type = st.radio(
    "Repository Input",
    ["ZIP Archive", "Local Folder"],
    horizontal=True
)

target_path = None

if input_type == "ZIP Archive":
    uploaded_zip = st.file_uploader("Upload repository ZIP archive", type=["zip"])
    
    if uploaded_zip is not None:
        st.session_state["uploaded_zip_file"] = uploaded_zip

    if "uploaded_zip_file" in st.session_state and st.session_state["uploaded_zip_file"] is not None:
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(st.session_state["uploaded_zip_file"], "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        target_path = temp_dir
        st.success("ZIP archive successfully extracted and ready for analysis.")

elif input_type == "Local Folder":
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("Browse..."):
            chosen_dir = safe_open_folder_dialog()
            if chosen_dir:
                st.session_state["folder_path"] = chosen_dir
            else:
                st.error("Native folder browser is unavailable in Cloud environment. Please paste path below.")

    with col2:
        folder_path = st.text_input(
            "Select or paste full folder path here:",
            value=st.session_state.get("folder_path", ""),
            placeholder="e.g. C:\\Users\\you\\Projects\\my-repo or /home/you/my-repo"
        )
        if folder_path:
            if os.path.exists(folder_path):
                target_path = folder_path
            else:
                st.error("Specified path does not exist on the server environment.")

# Execution Trigger
if target_path:
    st.info(f"Target path configured: `{target_path}`")
    if st.button("Run Cryptographic Scan", type="primary"):
        with st.spinner("Analyzing codebase and extracting cryptographic artefacts..."):
            findings = scan_repository(target_path)
            risk_assessment = calculate_mosca_risk(findings, z_horizon)
            recommendations = get_pqc_recommendations(findings)
            cbom = generate_cbom(findings)

            st.success("Analysis completed successfully!")

            st.divider()
            st.header("Unified Cryptographic Asset Inventory & Findings")
            if findings:
                st.json(findings)
            else:
                st.warning("No cryptographic assets or vulnerable algorithms detected in the selected target.")

            st.header("Quantum Risk Assessment (Mosca's Theorem)")
            st.json(risk_assessment)

            st.header("Post-Quantum Cryptography (PQC) Migration Roadmap")
            st.json(recommendations)

            st.header("Generated CBOM Inventory")
            st.json(cbom)
