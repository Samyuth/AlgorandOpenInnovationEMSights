from beaker import localnet, client
from algosdk.encoding import decode_address
from algosdk import kmd, wallet, account, transaction

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


if __name__ == "__main__":
    # Create accounts and dispense funds
    new_accounts = add_new_accounts()
    dispense_funds(new_accounts)

    client = localnet.get_algod_client()

    # get accounts
    accounts = localnet.kmd.get_accounts()

    print(len(accounts))
    print()
    print()
    print(client.account_info(accounts[0].address)['amount'])

    for acc in new_accounts:
        print(client.account_info(acc[1])['amount'])