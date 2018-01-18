# Sea Watch

![alt text](./temporary-logo.png)

Simple observer that rebuilds and updates single Docker services when their code changes.


## Usage

1. Make sure Python (including pip) is installed.
2. Install project dependencies like so:
```
$ pip install -r requirements.txt
```
3. Run the _run.py_ script poiting to the _docker-compose.yml_:
```
$ python run.py <path to docker-compose.yml>
```

__Sea Watch__ will now wait for source code changes and automatically update the services within their Docker Compose environment.
