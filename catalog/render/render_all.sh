#!/bin/bash
cd "$(dirname "$0")"; mkdir -p ../img
for k in panel panel_groove membrane insulation lprofile tprofile vprofile anchor rivet screw washer gasket tape epdm cartridge primer activator clip dowel; do ./shoot.sh $k ../img/c_$k.png 1200 900; done
./shoot.sh bracket_fixed ../img/c_bracket_fixed.png 1200 900 "&yaw=-1.0"
./shoot.sh bracket_sliding ../img/c_bracket_sliding.png 1200 900 "&yaw=-1.0"
for k in laser drill riveter hand_riveter drillbit jig saw tracksaw cnc router level clamp suction gun brush wipes knife glasses ear gloves mask boots hammerdrill calipers square hygro deburr vacuum wrench; do ./shoot.sh $k ../img/t_$k.png 1200 800; done
./shoot.sh tape_measure ../img/t_tape.png 1200 800
python3 autocrop.py ../img
