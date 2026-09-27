# ECDAT — Enterprise Cryptographic Discovery & Analysis Tool

ECDAT scans source files, dependency manifests, protocol/configuration files, binaries, certificates, repositories, and container images for cryptographic artefacts. It produces normalized findings, risk analysis, PQC recommendations, and CBOM exports.

## Run locally

1. Use Python 3.10 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Deploy on Streamlit Community Cloud

1. Push the contents of this project folder to the root of a GitHub repository.
2. In Streamlit Community Cloud, select that repository, branch, and `app.py` as the main file.
3. Ensure `requirements.txt` is at the repository root.
4. For a hosted app, use the **ZIP Archive** repository input option to upload a project ZIP. The local-folder picker is intended for a desktop environment; a hosted Streamlit app cannot browse folders on your personal computer.

## Scanner package

The `scanners/` package is required by `scanner.py` and `repository_scanner.py`. Keep the package and its `__init__.py` in the repository:

- `scanners/source_scanner.py`
- `scanners/dependency_scanner.py`
- `scanners/protocol_scanner.py`
- `scanners/binary_scanner.py`
- `scanners/config_scanner.py`
- `scanners/certificate_scanner.py`

## Container test fixture

The large generated `container_test/pqc-test-image.tar` fixture is not included in the GitHub-ready archive because it is over GitHub's 100 MB per-file limit. The test source and Dockerfile are retained; rebuild the fixture locally from `container_test/` if needed:

```bash
cd container_test
docker build -t pqc-test-image .
```

## Notes

- Historical `app_backup_*.py` and engine backup files are retained for reference; Streamlit's entry point remains `app.py`.
- `.git` history, Python bytecode/cache folders, and `.DS_Store` files are omitted from the distribution ZIP. They are not required to run the application.
