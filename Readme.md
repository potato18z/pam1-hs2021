# Repository for ETH HS 2021 PAM I course
If you prefer to run the notebooks locally, it is recommended to create a virtual environment. Please perform subsequent instructions.

## Virtual Python environment
You need to install [Python3](https://www.python.org/) first.
### Install the ```pyAcceLEGOrator```(any name you like) environment
#### Option 1: Installation using virtualenv (for python 2 and 3)
If you do not have ```virtualenv``` installed, first install it:
```bash
$ pip install virtualenv
```

Then create and activate the environment:
```bash
$ virtualenv -p `which python3` your_place/pyAcceLEGOrator.venv
$ source your_place/pyAcceLEGOrator.venv/bin/activate
```
#### Option 2: Installation using venv (only for python 3)
```bash
$ python3 -m venv your_place/pyAcceLEGOrator.venv
$ source your_place/pyAcceLEGOrator.venv/bin/activate
```
### Install required packages and kernel
Install packages from `requirements.txt` in the *activated* environment

```bash
(pyAcceLEGOrator.venv)$ pip install -r requirements.txt
```

Add the virtual environment as a python kernel, so that you can import packages inside jupyter
```bash
(pyAcceLEGOrator.venv)$ ipython kernel install --name "pyAcceLEGOrator.venv" --user
```

## Run Jupyter
A Jupyter notebook is started by executing

```bash
(pyAcceLEGOrator.venv)$ jupyter notebook
```
If there's kernel error, just choose the "pyAcceLEGOrator.venv" kernel.

## Deactivate virtual environment
The virtual environment can be deactivated with

```bash
(pyAcceLEGOrator.venv)$ deactivate
```
