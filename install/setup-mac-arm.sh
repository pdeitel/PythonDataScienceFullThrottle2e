#!/usr/bin/env bash
# setup-mac-arm.sh — Full environment setup for Apple Silicon (M1/M2/M3/M4)
#
# Usage: bash setup-mac-arm.sh
#
# What this does:
#   1. Creates (or updates) the pydsft conda environment
#   2. Downloads spaCy models
#   3. Downloads TextBlob corpora
#   4. Downloads NLTK data
#   5. Verifies the key packages load correctly

set -euo pipefail   # exit on error, unset variable, or pipe failure

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_NAME="pydsft"
YML="$SCRIPT_DIR/environment-mac-arm.yml"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " pydsft — Mac ARM setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Step 1: Create or update the conda environment ──────────────────────────
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "▶ Environment '${ENV_NAME}' already exists — updating..."
    conda env update -n "$ENV_NAME" -f "$YML" --prune
else
    echo "▶ Creating environment '${ENV_NAME}'..."
    conda env create -f "$YML"
fi

# ── Step 2: spaCy models ─────────────────────────────────────────────────────
echo "▶ Downloading spaCy models..."
conda run -n "$ENV_NAME" python -m spacy download en_core_web_sm
conda run -n "$ENV_NAME" python -m spacy download en_core_web_md
conda run -n "$ENV_NAME" python -m spacy download en_core_web_lg

# ── Step 3: TextBlob corpora ─────────────────────────────────────────────────
echo "▶ Downloading TextBlob corpora..."
conda run -n "$ENV_NAME" python -m textblob.download_corpora

# ── Step 4: NLTK data ────────────────────────────────────────────────────────
echo "▶ Downloading NLTK data..."
conda run -n "$ENV_NAME" python -c "
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('stopwords')
"

# ── Step 5: Smoke test ───────────────────────────────────────────────────────
echo "▶ Verifying key packages..."
conda run -n "$ENV_NAME" python -c "
import sklearn
import tensorflow as tf
import pyspark
import spacy
import nltk
import textblob
print('✓ scikit-learn', sklearn.__version__)
print('✓ TensorFlow  ', tf.__version__)
print('✓ PySpark     ', pyspark.__version__)
print('✓ spaCy       ', spacy.__version__)
print('All packages OK')
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Setup complete!"
echo " To activate: conda activate ${ENV_NAME}"
echo " To launch:   jupyter lab"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
