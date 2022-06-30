# \[pyforge3\] compound data tool

Compound Data Tool is a useful CLI application which allows you to:
* download summary information about compounds from open API resources
* show the summary information in a fancy way from the local storage

## Build

### Prerequisities
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
```bash
# checkout
git clone git@github.com:drnk/pyforge3.git pyforge3 && cd pyforge3

# build and run
docker-compose build && docker-compose up -d
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