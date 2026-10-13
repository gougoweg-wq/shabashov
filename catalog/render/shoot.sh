#!/bin/bash
# usage: shoot.sh name out.png [w h extra-query]
C=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
W=${3:-800}; H=${4:-600}
$C --headless --no-sandbox --use-angle=swiftshader --enable-unsafe-swiftshader --hide-scrollbars \
  --default-background-color=00000000 --window-size=$W,$((H+200)) --virtual-time-budget=60000 --run-all-compositor-stages-before-draw \
  --screenshot="$2" "http://localhost:8765/scene.html?name=$1&w=$W&h=$H$5" >/dev/null 2>&1
python3 -c "import sys;from PIL import Image;im=Image.open(sys.argv[1]);im.crop((0,0,$W,$H)).save(sys.argv[1])" "$2"
# retry once if the frame came out empty (asset load timing)
if python3 -c "import sys;from PIL import Image;sys.exit(0 if Image.open(sys.argv[1]).getbbox() else 1)" "$2"; then :; else
  $C --headless --no-sandbox --use-angle=swiftshader --enable-unsafe-swiftshader --hide-scrollbars \
    --default-background-color=00000000 --window-size=$W,$((H+200)) --virtual-time-budget=120000 --run-all-compositor-stages-before-draw \
    --screenshot="$2" "http://localhost:8765/scene.html?name=$1&w=$W&h=$H$5" >/dev/null 2>&1
  python3 -c "import sys;from PIL import Image;im=Image.open(sys.argv[1]);im.crop((0,0,$W,$H)).save(sys.argv[1])" "$2"
fi
