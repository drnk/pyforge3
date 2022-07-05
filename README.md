# \[pyforge3\] compound data tool

Compound Data Tool is a fancy and useful CLI application which allows you to:
* download summary information about compounds from open API resources
* show the summary information in a fancy way from the local storage

---

## Build

> :warning: **All below commands are running from the project root directory**

### Prerequisities
* git
* Docker
* docker-compose

Verified at versions:
    
```bash
$ docker --version
Docker version 20.10.17, build 100c701

$ docker-compose --version
Docker Compose version v2.3.4
```

### Build and Run

Checkout the code:

```bash
# checkout
git clone git@github.com:drnk/pyforge3.git pyforge3 && cd pyforge3
```

Build and run configured containers from the root project directory (where [docker-compose.yml](docker-compose.yml) file located)

```bash
# build and run
docker-compose -p pyforge3 build && docker-compose -p pyforge3 up -d
```

### Use
Run the `cli` container

```bash
docker run --network=pyforge3_appnetwork --env-file=.env.dev -it pyforge3_cli
```

From the container you are able to use `cdt` tool:
```
app@be94926f743d:/usr/src/app$ cdt --help                                     
Usage: cdt [OPTIONS] COMMAND [ARGS]...                                        
                                                                              
  Compound-data-tool or CDT is a command line tool allows you to actualize the
  information about compounds.                                                
                                                                              
Options:                                                                      
  -v, --verbose  Enables verbose mode.                                        
  --version      Show the version and exit.                                   
  --help         Show this message and exit.                                  
                                                                              
Commands:                                                                     l
  actualize  Actualizing compound data from the open source APIs.             
  show                                                                        
  supported  Information about supported compounds.
```

or another example with actualizing information:

```
app@be94926f743d:/usr/src/app$ cdt actualize 18W
-------------------------------------           
|              name | value         |           
|-----------------------------------|           
|          compound | 18W           |           
|              name | 3-[(5Z)-5-... |           
|           formula | C20 H22 N2 O9 |           
|             inchi | InChI=1S/C... |           
|         inchi_key | MBSNQHZDAB... |           
|            smiles | Cc1c(c(c([... |           
| cross_links_count | 2             |           
-------------------------------------           
app@be94926f743d:/usr/src/app$
```

---
## Local Development

For local development you have to obtain Postgres running instance. Update your local [.env.dev](.env.dev) file data.

Another (preferable) option is to run docker PostgreSQL image by:
```bash
docker-compose -p pyforge3 build && docker-compose -p pyforge3 up -d
```
In that way, connection to database will be established automatically if the PostgreSQL container is running in WSL.

### Prepare environment
It is highly recommended to use virtual environment for development purposes. Use `pyenv` or `virtual-env` or `venv` or what you like. Activate the environment and install the python packages via `pip`:
```bash
python -m pip install -U pip wheel setuptools && pip install -r services/app/requirements.dev.txt
```

### Testing

For test running use:
```bash
pytest -vv -ra --cov=src --cov=storage
```

### Run

For convinient use of `cdt` tool from command line install it as a package:
```bash
pip install --editable services/app
```

After that you are able to use `cdt`. For example:
```bash
cdt supported
```