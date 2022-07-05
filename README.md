# \[pyforge3\] compound data tool

Compound Data Tool is a fancy and useful CLI application which allows you to:
* download summary information about compounds from open API resources
* show the summary information in a fancy way from the local storage

---
## How to work with Compound Data Tool

### Actualizing Compound Summary
Common user use-case starting with the actualizing procedure. When the user wants to actualize local compound information from the Open Public API. For that purpose, use `actualize` sub-command. For example, command for actualization of `ATP` compound will looks like:
```
$ cdt actualize --full ATP
-----------------------------------------------------------------------------------
|              name | value                                                       |
|---------------------------------------------------------------------------------|
|          compound | ATP                                                         |
|              name | ADENOSINE-5'-TRIPHOSPHATE                                   |
|           formula | C10 H16 N5 O13 P3                                           |
|             inchi | InChI=1S/C10H16N5O13P3/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(1 |
|                   | 7)6(16)4(26-10)1-25-30(21,22)28-31(23,24)27-29(18,19)20/h2- |
|                   | 4,6-7,10,16-17H,1H2,(H,21,22)(H,23,24)(H2,11,12,13)(H2,18,1 |
|                   | 9,20)/t4-,6-,7-,10-/m1/s1                                   |
|         inchi_key | ZKHQWZAMYRWXGA-KQYNXXCUSA-N                                 |
|            smiles | c1nc(c2c(n1)n(cn2)C3C(C(C(O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O) |
|                   | O)O)N                                                       |
| cross_links_count | 22                                                          |
-----------------------------------------------------------------------------------
```
By specifying `--full` option you will be able to see the full information which gets into local database without any cuts. By default you will see only cut values (which are longer then 13 characters)

### Retreiving Compound Summary
After actualizing the information you will be able to retreive compound summary by execution:
```bash
cdt show --full ATP
```
Option `--full` is working in the same manner as described before and you'll get the same result as for `actualize` plus the `updated` field which contains information about when that entity was updated.

Another useful command provides you an information about locally stored compound summary:
```
$ cdt ls
-------------------------------------
| name | updated_at                 |
|------+----------------------------|
| ATP  | 2022-07-05T13:19:46.995453 |
| 18W  | 2022-07-05T13:25:06.095516 |
-------------------------------------
```

### Supported Compounds
For list of supported compounds use `supported` sub-command. For example:
```
$ cdt supported
Next compounds are supported by cdt:
  ADP
  ATP
  STI
  ZID
  DPM
  XP9
  18W
  29P
```

### Delete Compound Summary Locally
In case you would like to get rid of some specific compound summary, use `remove` sub-command. For example:
```
$ cdt remove ATP
Compound ATP succesfully removed.
```

---

## Build Compound Data Tool

Below section describe how to run `cdt` in Docker containers using `docker-compose`.

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

### Build Images and Run Containers

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

### Work with CDT within Docker container
Run the `pyforge3_cli` container

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

---

## Logging

For troubleshooting and debugging purposes it is possible to obtain the logs of `cdt`.

By default, the application logs are writing to the `console.log` file in the root folder of the project.

If you a lazy person and like the hardcore, check the `-v/--verboose` option of command line. By setting it immediate after `cdt` token you will receive the `DEBUG` level logs into the `STDOUT`. This is switched off by default. For example:

```
3$ cdt -v supported
2022-07-05 16:34:44,053 INFO sqlalchemy.engine.Engine select pg_catalog.version()
2022-07-05 16:34:44,053 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-07-05 16:34:44,055 INFO sqlalchemy.engine.Engine select current_schema()
2022-07-05 16:34:44,055 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-07-05 16:34:44,056 INFO sqlalchemy.engine.Engine show standard_conforming_strings
2022-07-05 16:34:44,056 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-07-05 16:34:44,058 INFO sqlalchemy.engine.Engine select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
2022-07-05 16:34:44,058 INFO sqlalchemy.engine.Engine [generated in 0.00031s] {'name': 'compounds_summary'}
2022-07-05 16:34:44,061 - [root] - [DEBUG] - COMMAND supported()
Next compounds are supported by cdt:
  ADP
  ATP
  STI
  ZID
  DPM
  XP9
  18W
  29P
$
```