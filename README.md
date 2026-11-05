# SVD Group 5 Simulations

## 1. First-Time Setup (VS Code)

**1. Clone & open in VS Code terminal (`Ctrl + ~`):**
```bash
git clone [https://github.com/atciamb/SVD_Group5_Sims.git]
cd SVD_Group5_Sims
code .
```

**2. Install isolated Python environment (`.venv`):**
- **Windows:** `.\setup_env.bat`
- **Mac/Linux:** `bash setup_env.sh`

*VS Code automatically activates `.venv` via `.vscode/settings.json`.*
---

## 2. Git Cheat Sheet
- **Pull latest updates (always start with this):**
  ```bash
  git pull
  ```
- **Upload your changes:**
  ```bash
  git add .
  git commit -m "Few words describing what you did"
  git push
  ```
- **Add a new Python package for the team:**
  ```bash
  pip install <package_name>
  pip freeze > requirements.txt
  ```
