# JAFFLE SHOP DuckDB Metabase

The initial structure of this project is based on the very famous Jaffle Shop exemple project from dbt-labs: <https://github.com/dbt-labs/jaffle-shop>

## Setup

### Create python venv and install the project dependancies

```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Copy the default dbt profiles

```sh
cp profiles.yml.default profiles.yml
```

### Install dbt dependancies

```sh
dbt deps
```

### Test your installation

This command performs a series of check and at the end you should be rewarded with `All checks passed!`

```sh
dbt debug
```

### Populate the database

For this step, Im using a pyairbyte ingestion pipeline CSV -> DuckDB.
The CSV connector is supported for python3 < 3.12 so I had to run my script in a container.  

- Image Building from this folder

```sh
docker build -f pyairbyte.Dockerfile -t pyairbyte .
```

- Run the container

```sh
docker run --name pyairbyte-0-25-0 -v ./jaffle-data:/source/jaffle-data:ro -v ./dev.duckdb:/destination/dev.duckdb pyairbyte
```

- Note: the first run is alway kind of slow because the connector have to be loaded
To re-run the ingestion script with outputs:

```sh
docker start -a pyairbyte-0-25-0
```

If you are not confortable using pyairbyte, you can also install airbyte locally on your machine using [abctl](https://github.com/airbytehq/abctl) and use the UI and other features but this will be a much heavier process to run.

### Have a look in your database

At this point, you can interract with the newly created and popultated database (`CTRL + D` to Quit the interractive command line).
If you dont have duckdb CLI installed: <https://duckdb.org/docs/installation/?version=stable&environment=cli&platform=linux&download_method=direct&architecture=x86_64>

```sh
duckdb dev.duckdb
```

Then execute the following query:

```sql
select * from raw.raw_customers limit 10;
```

### Build the models

```sh
dbt build
```

Note: you should get couple of warnings, they are completely normal because it is the initial run

### Run Metabase interface with duckdb community driver

Source of the dockerfile: <https://github.com/dbt-labs/jaffle_shop_duckdb>

For this step, you will need Docker engine installed on your machine. If (like me) you live in a cave and don't know how to install docker: <https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository>
For the guys in the back (like me as well) who dont want to spell the magic word each time (also usefull for docker vscode extention): <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>

- Build the docker image

```sh
docker build -f metabase-duckdb.Dockerfile -t metabase-duckdb .
```

- Run docker image with Metabase state persistance and read-only (`:ro`) connection to the duckdb:

```sh
docker run -d -p 3000:3000 -m 2GB \
-v metabase-data:/metabase-data \
-v ./dev.duckdb:/container/directory/dev.duckdb:ro \
--name metabase-duckdb metabase-duckdb
```

- Access Metabase: <http://localhost:3000>

- Fill the form, at driver / database type, choose duckdb. Next, in the settings page of DuckDB of Metabase Web UI you could set your DB file name like this `/container/directory/dev.duckdb`
- Toggle `Establish a read-only connexion` ON

Useful Docker commands

- `docker ps`: list running containers
- `docker stop metabase-duckdb`: stop the running container (after first run or if is started)
- `docker start metabase-duckdb`: start running the container (no need to provide db path like first run)
