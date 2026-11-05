# SVD Group 5 Simulations

## Folders
- **`ADCS_Sims/`** – Attitude Determination & Control (`adcs_sim.py`)
- **`Payload_Sims/`** – Payload analysis (`payload_sim.py`)
- **`Structures_Sims/`** – Structural/mechanical (`structures_sim.py`)
- **`Thermal_Sims/`** – Thermal modeling (`thermal_sim.py`)

---

## 1. First-Time Setup (VS Code)

**1. Clone & open in VS Code terminal (`Ctrl + ~`):**
```bash
git clone [https://github.com/atciamb/SVD_Group5_Sims.git](https://github.com/atciamb/SVD_Group5_Sims.git)
cd SVD_Group5_Sims
code .
```

**2. Install isolated Python environment (`.venv`):**
- **Windows:** `.\setup_env.bat`
- **Mac/Linux:** `bash setup_env.sh`

*VS Code automatically activates `.venv` via `.vscode/settings.json`.*

---

## 2. Daily Git Cheat Sheet

- **Get latest updates (run before working):**
  ```bash
  git pull
  ```
- **Upload your changes:**
  ```bash
  git add .
  git commit -m "Describe changes"
  git push
  ```
- **Add a new Python package for the team:**
  ```bash
  pip install <package_name>
  pip freeze > requirements.txt
  ```
