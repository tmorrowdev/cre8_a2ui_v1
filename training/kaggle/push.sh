#!/usr/bin/env bash
# Upload training/data/{train,val}.jsonl as a private Kaggle dataset and push the
# fine-tune notebook to run on a free GPU.
#
# Needs: pip install kaggle, then `kaggle auth login` (or ~/.kaggle/kaggle.json).
# Usage: KAGGLE_USER=yourname training/kaggle/push.sh
set -euo pipefail
: "${KAGGLE_USER:?set KAGGLE_USER to your Kaggle username}"
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA="$HERE/../data"
SLUG="$KAGGLE_USER/a2ui-apps-composer-data"

for f in train.jsonl val.jsonl; do
  [[ -s "$DATA/$f" ]] || { echo "missing $DATA/$f — run scripts/distill.py first" >&2; exit 1; }
done

STAGE="$(mktemp -d)"
cp "$DATA/train.jsonl" "$DATA/val.jsonl" "$STAGE/"
cat > "$STAGE/dataset-metadata.json" <<JSON
{"title": "a2ui-apps-composer-data", "id": "$SLUG", "licenses": [{"name": "other"}]}
JSON
if kaggle datasets status "$SLUG" >/dev/null 2>&1; then
  kaggle datasets version -p "$STAGE" -m "refresh $(date +%F)"
else
  kaggle datasets create -p "$STAGE"   # private by default
fi

KDIR="$(mktemp -d)"
cp "$HERE/finetune.ipynb" "$KDIR/"
sed "s/YOUR_KAGGLE_USERNAME/$KAGGLE_USER/g" "$HERE/kernel-metadata.json" > "$KDIR/kernel-metadata.json"
kaggle kernels push -p "$KDIR"
echo "Pushed. First run only: on kaggle.com set Accelerator GPU T4 x2 + Internet on, attach the HF_TOKEN secret, set HF_REPO, then Save & Run All."
