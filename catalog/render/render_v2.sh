#!/bin/bash
cd "$(dirname "$0")"; O=../img/v2; mkdir -p $O
C=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
coords(){ $C --headless --no-sandbox --use-angle=swiftshader --enable-unsafe-swiftshader --virtual-time-budget=60000 --run-all-compositor-stages-before-draw --window-size=$3,$4 --dump-dom "http://localhost:8765/scene.html?name=$1&w=$3&h=$4$5" 2>/dev/null | grep -o '<pre id="out">[^<]*' | sed 's/<pre id="out">//' > $O/$2.json; }
./shoot.sh x_cover $O/cover.png 1080 1920 "&dec=F-24"
for s in rivet glue hidden screw; do ./shoot.sh x_expl_$s $O/expl_$s.png 1200 1460; coords x_expl_$s expl_$s 1200 1460; done
for s in rivet glue hidden screw; do ./shoot.sh x_sys_$s $O/sys_$s.png 1000 1100; done
for s in rivet screw; do ./shoot.sh x_macro_$s $O/macro_$s.png 1000 760; done
for s in glue hidden; do ./shoot.sh x_macro_$s $O/macro_$s.png 1000 760 "&v=top"; done
./shoot.sh x_wall_rivet $O/wall_rivet.png 1080 1920 "&dec=F-11&head=%233c3d40"
./shoot.sh x_wall_rivet $O/wall_rivet_close.png 1000 760 "&dec=F-20&head=%23aaa39b&cx=1700&cy=2600&cz=2100&tx=500&ty=3700&fov=42"
./shoot.sh x_wall_screw $O/wall_screw.png 1000 760 "&dec=F-30&head=%234a4a4c&cx=4200&cy=1500&cz=4400&fov=40"
./shoot.sh x_wall_glue $O/wall_glue.png 1000 760 "&dec=F-35&cx=4200&cy=1500&cz=4400&fov=40"
./shoot.sh x_wall_hidden $O/wall_hidden.png 1000 760 "&dec=F-32&cx=4200&cy=1500&cz=4400&fov=40"
./shoot.sh x_wall_rivet $O/wall_rivet2.png 1000 760 "&dec=F-11&head=%233c3d40&cx=4200&cy=1500&cz=4400&fov=40"
./shoot.sh building $O/b_rivet.png 1080 1920 "&big=1&fix=rivet&d1=F-11&d2=F-38&head=%233c3d40"
./shoot.sh building $O/b_glue.png 1080 1920 "&big=1&d1=F-35&d2=F-11"
./shoot.sh building $O/b_hidden.png 1080 1920 "&big=1&d1=F-30&d2=F-38&v=1"
./shoot.sh building $O/b_screw.png 1080 1920 "&big=1&fix=screw&d1=F-12&d2=F-35&head=%234a4a4c"
./shoot.sh building $O/b_dusk.png 1080 1920 "&big=1&dark=1&d1=F-11&d2=F-35"
for s in rivet glue hidden screw; do ./shoot.sh building $O/bw_$s.png 1000 760 "&big=1$( [ $s = rivet ] && echo '&fix=rivet&d1=F-11&d2=F-38' )$( [ $s = glue ] && echo '&d1=F-35&d2=F-11' )$( [ $s = hidden ] && echo '&d1=F-30&d2=F-38&v=1' )$( [ $s = screw ] && echo '&fix=screw&d1=F-12&d2=F-35' )"; done
