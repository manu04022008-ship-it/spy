# ECDAT — Enterprise Cryptographic Discovery & Analysis Tool

ECDAT is a Streamlit application for discovering cryptographic artefacts in source files and ZIP archives, organizing findings into a cryptographic inventory, estimating quantum-related risk, and generating CBOM-style reports and PQC migration recommendations.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push the contents of this folder to the root of a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Select branch `main` and main file `app.py`.
4. Deploy.

The `scanners/` directory must remain next to `app.py` and `scanner.py`.

## Important deployment notes

- For a public cloud deployment, choose **ZIP Archive** and upload a source-code repository ZIP. A path on your personal computer is not accessible to the cloud server.
- The **Local Folder** and **Browse** options are intended for a local run. The browser's folder picker does not browse your personal computer from a hosted Streamlit server.
- Live Docker image scanning requires access to a Docker Engine. Streamlit Community Cloud generally does not provide a Docker daemon, so that feature may not work in the hosted app.
- Scan only repositories and files you are authorized to analyze. Avoid uploading secrets, private keys, credentials, or confidential source code to a public app.
- Findings and migration suggestions are automated analysis aids. Validate results before making production cryptographic changes. The migration simulation is illustrative and does not modify the original source code.

## Project structure

```text
.
├── app.py
├── scanner.py
├── repository_scanner.py
├── container_scanner.py
├── unified_inventory.py
├── mosca_engine.py
├── cbom_formatter.py
├── pqc_recommendations.py
├── algorithm_patcher.py
├── requirements.txt
└── scanners/
    ├── __init__.py
    ├── source_scanner.py
    ├── dependency_scanner.py
    ├── protocol_scanner.py
    ├── binary_scanner.py
    ├── config_scanner.py
    └── certificate_scanner.py
```
