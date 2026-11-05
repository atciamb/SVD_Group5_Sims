# SVD Group 5 Simulations

## Subsystem Folders
- **ADCS_Sims**: Attitude Determination and Control System simulations (`adcs_sim.py`)
- **Payload_Sims**: Payload simulations and analysis (`payload_sim.py`)
- **Structures_Sims**: Structural and mechanical simulations (`structures_sim.py`)
- **Thermal_Sims**: Thermal modeling and simulations (`thermal_sim.py`)

---

## 1. First-Time Workspace & Python Setup (VS Code)

### Step A: Clone the Repository
Open the terminal in VS Code (`Ctrl + ~`) and run:
```bash
git clone https://github.com/atciamb/SVD_Group5_Sims.git
cd SVD_Group5_Sims
code .
```

### Step B: Set Up the Isolated Python Environment (One Command)
To install all required simulation packages into an isolated local `.venv` folder (without affecting your existing Python installation), run the setup script in your VS Code terminal:

- **Windows (PowerShell / CMD):**
  ```powershell
  .\setup_env.bat
  ```
- **Mac / Linux:**
  ```bash
  bash setup_env.sh
  ```

> **Note:** Our `.vscode/settings.json` file automatically configures VS Code to use `.venv` as your Python interpreter and activates it whenever you open a new terminal (`(.venv)` will appear at the start of your prompt).
>
> *Alternative VS Code GUI method:* Press `Ctrl + Shift + P`, type **Python: Create Environment**, select **Venv**, choose your Python version, and check `requirements.txt`.

---

## 2. Daily Git Commands Cheat Sheet

### Before you start working (Download teammates latest updates)
Always run this first before editing files so your workspace is up to date:
```bash
git pull
