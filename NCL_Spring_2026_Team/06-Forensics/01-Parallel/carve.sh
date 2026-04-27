#!/bin/bash
# Carve the 6 images appended after %%EOF in chip_design_howto.pdf
# Run from inside /home/kali/NCL/NCL_Spring_2026_Team/06-Forensics/01-Parallel
set -e

PDF="chip_design_howto.pdf"
[ -f "$PDF" ] || { echo "ERROR: $PDF not found in $(pwd)"; exit 1; }

# offset  size     output
carve() {
    dd if="$PDF" of="$3" bs=1 skip="$1" count="$2" status=none
    echo "  wrote $3 ($2 bytes)"
}

echo "Carving images..."
carve 1245754  94123 img_1.png
carve 1339877  74554 img_2.jpg
carve 1414431 338025 img_3.png
carve 1752456  49027 img_4.jpg
carve 1801483 152357 img_5.png
carve 1953840 195198 img_6.png

echo
echo "Done. Verifying file types:"
file img_*.png img_*.jpg
