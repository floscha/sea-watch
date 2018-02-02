# Sea Watch

![alt text](./temporary-logo.png)

Simple observer that rebuilds and updates single Docker services when their code changes.


## Usage

1. Make sure Python (including pip) is installed.
2. From within the project folder, install _Sea Watch_ like so:
```
$ pip install .
```
3. Run the command line script pointing to the _docker-compose.yml_ and specify what file extensions to observe:
`
$ seawatch docker-compose.yml py
`
for example uses the _docker-compose.yml_ file in the current directory and observes files with an _.py_ extension.

__Sea Watch__ will now wait for source code changes and automatically update the services within their Docker Compose environment.
