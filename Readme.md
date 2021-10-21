# Repository for ETH HS 2021 PAM I course
If you prefer to run the notebooks locally, it is recommended to create a virtual environment. Please perform subsequent instructions.

## Virtual Python environment
You need to install [Python3](https://www.python.org/) first.
The ```pyAcceLEGOrator```(any name you like) environment is installed with following steps:
### Option 1: Installation using virtualenv (for python 2 and 3)
If you do not have ```virtualenv``` installed, first install it:
```bash
pip install virtualenv
```

Then create and activate the environment:
```bash
virtualenv -p `which python3` your_place/pyAcceLEGOrator.venv
source your_place/pyAcceLEGOrator.venv/bin/activate
```

Install packages from `requirements.txt` in the *activated* environment

```bash
pip install -r requirements.txt
```

### Option 2: Installation using venv (only for python 3)
```bash
python3 -m venv your_place/pyAcceLEGOrator.venv
source your_place/pyAcceLEGOrator.venv/bin/activate
```

Install packages from `requirements.txt` in the *activated* environment

```bash
pip install -r requirements.txt
```

## Run Jupyter
A Jupyter notebook is started by executing

```bash
jupyter notebook
```

## Deactivate virtual environment
The virtual environment can be deactivated with

```bash
deactivate
```
