![alt text](./temporary-logo.png)

# SeaWatch

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f0613cd30da64e4a92b7986ef8c3805c)](https://www.codacy.com/app/floscha/seawatch?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=floscha/seawatch&amp;utm_campaign=Badge_Grade)

Simple observer that rebuilds and updates single Docker services when their code changes.


## Usage

1. Make sure Python (including pip) is installed.
2. From within the project folder, install __SeaWatch__ like so:
```
$ pip install .
```
3. Run the command line script pointing to the _docker-compose.yml_ and specify what file extensions to observe:
```
$ seawatch docker-compose.yml py
```
The example above uses the _docker-compose.yml_ file in the current directory and observes all files with an _.py_ extension.
Also, it is possible to specify multiple file extensions to observe.

__SeaWatch__ will now wait for source code changes and automatically update the services within their Docker Compose environment.
