# `pydsft` — Local Conda Environment Setup

This folder contains conda environment definitions and setup scripts for running the notebooks locally. There are two configurations:

| File | Platform |
|------|----------|
| `environment-mac-arm.yml` | Apple Silicon (M1/M2/M3/M4) |
| `environment-win-x64.yml` | Windows x86-64 |
| `setup-mac-arm.sh` | Mac ARM setup script |
| `setup-win-x64.ps1` | Windows x64 setup script |

The setup scripts are the recommended way to install. They create the conda environment from the appropriate `.yml` file, then automatically run all required post-install steps (spaCy models, TextBlob corpora, NLTK data).

---

## Prerequisites

- **Conda** — [Anaconda](https://www.anaconda.com/download) or
  [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **Git** — required by pip to install any packages directly from GitHub
- **Mac ARM only:** Xcode Command Line Tools — run `xcode-select --install`
  if you have not done so already

---

## Mac ARM (Apple Silicon) Setup

Open a Terminal and run:

```bash
bash setup-mac-arm.sh
```

The script will:

1. Create (or update) the `pydsft` conda environment from `environment-mac-arm.yml`
2. Download the three spaCy English models (`sm`, `md`, `lg`)
3. Download the TextBlob corpora
4. Download the NLTK datasets (`punkt`, `punkt_tab`, `wordnet`, `stopwords`)
5. Run a smoke test confirming scikit-learn, TensorFlow, PySpark, and spaCy all import correctly

Once complete, activate the environment and launch JupyterLab:

```bash
conda activate pydsft
jupyter lab
```

## Windows x64 Setup

Open an **Anaconda PowerShell Prompt** and run:

```powershell
.\setup-win-x64.ps1
```

If you see an execution policy error, run this once first, then retry:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

The script performs the same steps as the Mac script (see above).

Once complete, activate the environment and launch JupyterLab:

```powershell
conda activate pydsft
jupyter lab
```
