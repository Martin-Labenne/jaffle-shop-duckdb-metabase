# Execute this file using chmod +x duckdb_venv_install.sh
# Then ./duckdb_venv_install.sh

# Approach: install directly in venv/bin so that it is accessible after venv activation
# When bumping the version, it will automatically overwrite the previous binary

VERSION=1.2.1
wget -O duckdb.zip https://github.com/duckdb/duckdb/releases/download/v$VERSION/duckdb_cli-linux-amd64.zip
unzip duckdb.zip -d venv/bin/
rm duckdb.zip
chmod +x venv/bin/duckdb

# When you will activate your venv, you will be able to access the duckdb cli at the appropriate version 