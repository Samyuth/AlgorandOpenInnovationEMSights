# EMSights

## Installation

All code contained in this repository depends on various components of algokit. Follow the installation instrucitons for Algokit [here](https://developer.algorand.org/docs/get-started/algokit/).

Create a virtual environment named `.venv` to install python dependencies. Activate the local environment and install the requirements folder using:
```
pip install -r requirements.txt
```

## Directory structure

Contract code in this repo is held in the emsights.py file and a demonstration of the methods is in deploy.py.

## Running Code

Start up the local net for algokit
```
algokit localnet start
```

Run the test script to examine a test run of the contract
```
python deploy.py
```

Stop the localnet
```
algokit localnet stop
```