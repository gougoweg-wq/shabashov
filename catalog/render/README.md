# 3D renders

Product, tool, node and building images in `../img/` are rendered with three.js in headless Chromium.

- CC0 models and HDRIs from Poly Haven (no attribution required): `python3 fetch_ph.py Drill_01 measuring_tape_01 garden_gloves_01 combination_wrench bench_vice_01 studio_small_09 kloofendal_48d_partly_cloudy_puresky evening_road_01_puresky`
- Everything else (profiles, brackets, rivets, panels, insulation, nodes, buildings) is modeled in `scenes.js`.
- `npm i`, start `python3 -m http.server 8765` here, then run `./render_all.sh` (products/tools) or `./shoot.sh node_base ../img/n_base.png 1400 1120`.
