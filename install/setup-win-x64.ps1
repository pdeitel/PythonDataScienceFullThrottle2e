# setup-win-x64.ps1 - Full environment setup for Windows x86-64
#
# Usage (from an Anaconda PowerShell Prompt):
#   .\setup-win-x64.ps1
#
# If you see an execution policy error, run this first:
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#
# What this does:
#   1. Creates (or updates) the pydsft conda environment
#   2. Downloads spaCy models
#   3. Downloads TextBlob corpora
#   4. Downloads NLTK data
#   5. Verifies the key packages load correctly

$ErrorActionPreference = "Stop"

$EnvName = "pydsft"
$YmlFile = Join-Path $PSScriptRoot "environment-win-x64.yml"

Write-Host "-----------------------------------------------------------"
Write-Host " pydsft - Windows x64 setup"
Write-Host "-----------------------------------------------------------"

# Step 1: Create or update the conda environment
$envExists = conda env list | Select-String "^$EnvName "
if ($envExists) {
    Write-Host "> Environment '$EnvName' already exists - updating..."
    conda env update -n $EnvName -f $YmlFile --prune
} else {
    Write-Host "> Creating environment '$EnvName'..."
    conda env create -f $YmlFile
}

# Step 2: spaCy models
Write-Host "> Downloading spaCy models..."
conda run -n $EnvName python -m spacy download en_core_web_sm
conda run -n $EnvName python -m spacy download en_core_web_md
conda run -n $EnvName python -m spacy download en_core_web_lg

# Step 3: TextBlob corpora
Write-Host "> Downloading TextBlob corpora..."
conda run -n $EnvName python -m textblob.download_corpora

# Step 4: NLTK data
Write-Host "> Downloading NLTK data..."
conda run -n $EnvName python -c @"
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('stopwords')
"@

# Step 5: Smoke test
Write-Host "> Verifying key packages..."
conda run -n $EnvName python -c @"
import sklearn
import tensorflow as tf
import pyspark
import spacy
import nltk
import textblob
print('OK scikit-learn', sklearn.__version__)
print('OK TensorFlow  ', tf.__version__)
print('OK PySpark     ', pyspark.__version__)
print('OK spaCy       ', spacy.__version__)
print('All packages OK')
"@

Write-Host ""
Write-Host "-----------------------------------------------------------"
Write-Host " Setup complete!"
Write-Host " To activate: conda activate $EnvName"
Write-Host " To launch:   jupyter lab"
Write-Host "-----------------------------------------------------------"
