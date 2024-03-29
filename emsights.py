from beaker import *
from pyteal import *

class EMSightsState:
    dispatcher = GlobalStateValue(TealType.bytes)
    emergency_queue = GlobalStateValue(TealType.bytes)
    queue_size = GlobalStateValue(TealType.uint64)

    # Role
    role = LocalStateValue(TealType.bytes)

    # User state
    name = LocalStateValue(TealType.bytes)
    age = LocalStateValue(TealType.uint64)
    allergies = LocalStateValue(TealType.bytes)
    medications = LocalStateValue(TealType.bytes)
    consent = LocalStateValue(TealType.bytes)
    device = LocalStateValue(TealType.bytes)
    responder = LocalStateValue(TealType.bytes)


emsights = Application("EMSights", state=EMSightsState())

@emsights.create
def create():
    return Seq(
        emsights.initialize_global_state(),
        emsights.state.dispatcher.set(Txn.sender())
    )

@emsights.opt_in
def opt_in():
    return Approve()

# An address registers as a patient
@emsights.external
def registerAsPatient(name : abi.String, age: abi.Uint16, allergies: abi.String, medications: abi.String):
    return Seq(
        emsights.state.role.set(Bytes("P")),
        (consent := abi.String()).set("FFFF"),
        emsights.state.name.set(name.get()),
        emsights.state.age.set(age.get()),
        emsights.state.allergies.set(allergies.get()),
        emsights.state.medications.set(medications.get()),
        emsights.state.consent.set(consent.get()),
    )

# An patient chooses to consent
@emsights.external
def patientConsent(consent : abi.String):
    return Seq(
        Assert(emsights.state.role == Bytes("P")),
        emsights.state.consent.set(consent.get())
    )

# A patient triggers an emergency
@emsights.external
def patientTriggerEmergency():
    return Seq(
        Assert(emsights.state.role == Bytes("P")),
        emsights.state.emergency_queue.set(Concat(emsights.state.emergency_queue, Txn.sender())),
        emsights.state.queue_size.set(emsights.state.queue_size + Int(32))
    )


# Patient registers a device
@emsights.external
def patientRegisterDevice(device : abi.Account):
    return Seq(
        Assert(emsights.state.role == Bytes("P")),
        emsights.state.device.set(device.address())
    )

# An address registers as a device
@emsights.external
def registerAsDevice():
    return emsights.state.role.set(Bytes("D"))

# Dispatcher chooses a responder to give access to a patients information
@emsights.external
def dispatcherSelectResponder(responder : abi.Account, patient : abi.Account):
    return Seq(
        Assert(Txn.sender() == emsights.state.dispatcher),
        App.localPut(patient.address(), Bytes("responder"), responder.address()),
        emsights.state.emergency_queue.set(Substring(emsights.state.emergency_queue.get(), Int(0), emsights.state.queue_size - Int(32))),
        emsights.state.queue_size.set(emsights.state.queue_size - Int(32))
    )

# Responder queries patient information
@emsights.external
def responderQueryInformation(patient : abi.Account, field : abi.String, *, output : abi.String):
    return Seq(
        Assert(App.localGet(patient.address(), Bytes("responder")) == Txn.sender()),
        output.set(App.localGet(patient.address(), field.get()))
    )

@emsights.external
def responderTransferCare(patient : abi.Account, reciever : abi.Account):
    return Seq(
        Assert(App.localGet(patient.address(), Bytes("responder")) == Txn.sender()),
        App.localPut(patient.address(), Bytes("responder"), reciever.address())
    )

if __name__ == "__main__":
    emsights.build().export("./artifacts")