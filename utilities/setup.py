from beaker import localnet
from algosdk import account, transaction
import subprocess

# generate new accounts
def add_new_accounts(n=3):
    # Create accounts
    new_accounts = []
    for _ in range(3):
        private, public = account.generate_account()
        localnet.kmd.add_account(private_key=private)
        new_accounts.append((private, public))

    return new_accounts

# Dispense funds from first account into the new accounts
def dispense_funds(new_accounts=[]):
    first_account = localnet.kmd.get_accounts()[0]

    client = localnet.get_algod_client()

    for reciever in new_accounts:
        paymenttxn = transaction.PaymentTxn(
            sender=first_account.address,
            receiver=reciever[1],
            amt=100000000,
            sp=client.suggested_params()).sign(first_account.private_key)
        
        client.send_transaction(paymenttxn)


# Function to start the account and initially dispense funds
def setup_accounts():
    #  Starting localnet if it hasn't already started
    try:
        node_status = localnet.get_algod_client().health()
    except:
        subprocess.run(["algokit", "localnet", "start"])

    accounts = localnet.kmd.get_accounts()

    # Different situations to add accounts or money
    if len(accounts) == 3:
        new_accounts = add_new_accounts()
        dispense_funds(new_accounts)
    elif len(accounts) < 6:
        new_accounts = add_new_accounts(6-len(accounts))
        dispense_funds(new_accounts)

    client = localnet.get_algod_client()
    accounts = localnet.kmd.get_accounts()

    # Further if any accounts don't have enough money first account will deposit
    dispense_list = []
    for acc in accounts:
        if client.account_info(acc.address)['amount'] == 0:
            dispense_list.append((acc.private_key, acc.address))
    dispense_funds(dispense_list)

# Function to redispense funds if needed
def redispense_funds():
    client = localnet.get_algod_client()
    accounts = localnet.kmd.get_accounts()

    # Dispense to accounts if the accounts have less than 100 algos
    dispense_list = []
    for acc in accounts:
        if client.account_info(acc.address)['amount'] < 100000000:
            dispense_list.append((acc.private_key, acc.address))
    dispense_funds(dispense_list)

if __name__ == "__main__":
    setup_accounts()
    redispense_funds()