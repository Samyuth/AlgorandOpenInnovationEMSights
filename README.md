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

### Setting up accounts

There are two ways to setup the environment before running the code:
1. Manually start up the local net and manipulate in dappflow
2. Use the setup.py file in utilities (recommended)

#### Manually setting up accounts

Start up the local net for algokit
```
algokit localnet start
```

Navigate to the KMD portal in Dappflow at https://app.dappflow.org/kmd-portal. Alternatively navigate here by opening Dappflow using
```
algokit localnet explore
```

Open the default unencrypted wallet and click connect without typing anything for the password. Upon connecting create two new accounts so that there are a total of 5 accounts. Add the new accounts to dev wallets. Navigate to the dev wallets portal at https://app.dappflow.org/dev-wallets and click dispense for the new accounts to dispense localnet funds to these accounts.

#### Running setup script

Navigate to the utilities directory and run setup.py
```
cd utilities
python setup.py
```

### Run the simulation

Run the test script to examine a test run of the contract
```
python deploy.py
```

### Stop the algorand localnet

Stop the localnet
```
algokit localnet stop
```