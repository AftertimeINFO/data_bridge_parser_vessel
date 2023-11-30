# Parser Vessel for aftertime project


### Deploy

#### Clone project
```commandline
git clone --recurse-submodules https://github.com/AftertimeINFO/data_bridge_parser_vessel.git
```

#### Library instalation
```commandline
pip install poetry
poetry install
```

#### Run parser
```commandline
poetry run python MarineTraffic.py --start --trace WORLD
```