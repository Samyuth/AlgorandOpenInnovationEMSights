from beaker import *
from pyteal import *

class OracleState:
    contract_admin = GlobalStateValue(TealType.bytes)

    prediction = LocalStateValue(TealType.bytes)

oracle = Application("Oracle", state=OracleState())

@oracle.create
def create():
    return Seq(
        oracle.initialize_global_state(),
        oracle.state.contract_admin.set(Txn.sender()),
        Approve()
    )

@oracle.opt_in
def opt_in():
    return Approve()

@oracle.update
def update():
    return Seq(
        Assert(oracle.state.contract_admin == Txn.sender()),
        Approve()
    )

@oracle.delete
def delete():
    return Seq(
        Assert(oracle.state.contract_admin == Txn.sender()),
        Approve()
    )

@oracle.external
def classificationNotify(prediction : abi.String):
    return Seq(
        App.localPut(Txn.sender(), Bytes("prediction"), prediction.get()),
        Approve()
    )