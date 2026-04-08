# [cloud-function-python]()

![license](https://img.shields.io/github/license/yadickson/cloud-function-python?style=flat-square)
[![build](https://img.shields.io/github/actions/workflow/status/yadickson/cloud-function-python/ci.yml?branch=main&style=flat-square)](https://github.com/yadickson/cloud-function-python/actions/workflows/ci.yml)
![tests](https://img.shields.io/endpoint?style=flat-square&url=https%3A%2F%2Fgist.githubusercontent.com%2Fyadickson%2F48c9e2094af5dbd32077ce69108c2b0e%2Fraw%2Fcloud-function-python-junit-tests.json)
![coverage](https://img.shields.io/endpoint?style=flat-square&url=https%3A%2F%2Fgist.githubusercontent.com%2Fyadickson%2F48c9e2094af5dbd32077ce69108c2b0e%2Fraw%2Fcloud-function-python-cobertura-coverage.json)


Copy file from SFTP to other SFTP server.


### Install python@3.12

```bash
brew install python@3.12
```

### Install environment

```bash
python3.12 -m venv .venv
```

### Activating environment

```bash
source .venv/bin/activate
```

### Install dependencies

```zsh
# zsh
pip install -e ".[dev,lint,test]"
```
```bash
# bash
pip install -e .[dev,lint,test]
```

### List all command

```bash
poetry run poe
```

### Format

```bash
poetry run poe format
```

### Lint

```bash
poetry run poe lint
```

### Duplicated

```bash
poetry run poe duplicated
```

### Test

```bash
poetry run poe test
```

### Coverage

```bash
poetry run poe test:coverage
```

### Mutation

```bash
poetry run poe test:mutation
```

### Build

```bash
poetry run poe build
```

### Run all previous steps

```bash
poetry run poe all
```

### Run local

```bash
poetry run poe start
```

```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.1.88:8080
```

### Check transfer

```bach
curl http://127.0.0.1:8080
```

### Deactivating environment

```bash
deactivate
```

###  Start application in debug mode

```bash
functions-framework --target execute --source main.py --signature-type http --debug
```