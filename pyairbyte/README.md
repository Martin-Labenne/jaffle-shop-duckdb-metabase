# Dev Container for pyAirbyte

## Image Building from this folder

```sh
docker build -f .devcontainer/dev-pyairbyte.Dockerfile -t dev-pyairbyte .
```

## Run the image and dev from VSCode

```sh
docker run -it --rm --name dev-pyairbyte-0-25-0 -v ./../jaffle-data:/source/jaffle-data:ro -v ./../dev.duckdb:/destination/dev.duckdb -v .:/workspace -w /workspace dev-pyairbyte bash
```

The above command is running the container in interactiv mode and clean it after exiting.
While the container is running, you can interact with is in VSCode thanks to the [dev-container extention](<https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers>)

- `-it`: Interact with the container in your terminal.
- `--rm`: Removes the container at the exit (so it's not left running or saved).
- `-v ./../jaffle-data/:/source/jaffle-data:ro`: Mounts the local `jaffle-data` folder read-only (`ro`) into the container at `/source/jaffle-data`.
- `-v ./../dev.duckdb:/destination/dev.duckdb`: Mounts the local DuckDB database file into `/destination/dev.duckdb` (read/write).
- `-v .:/workspace`: Mounts the current directory (`.`) into the container at `/workspace`
- `-w /workspace`: Sets the working directory inside the container to `/workspace` (i.e., the current folder from the host).
- `bash`: This is the command run inside the container: it starts an interactive bash shell.
