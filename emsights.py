from beaker import *
from pyteal import *
from beaker.lib.storage import BoxMapping

class PatientInfo(abi.NamedTuple):
    name: abi.Field[abi.String]
    age: abi.Field[abi.Uint16]
    allergies: abi.Field[abi.String]
    medications: abi.Field[abi.String]
    consent: abi.Field[abi.String]

class EMSightsState:
    patient_info = BoxMapping(abi.Address, PatientInfo)

    # Role
    role = LocalStateValue(TealType.bytes)

    # User state
    name = LocalStateValue(TealType.bytes)
    age = LocalStateValue(TealType.uint64)
    allergies = LocalStateValue(TealType.bytes)
    medications = LocalStateValue(TealType.bytes)
    consent = LocalStateValue(TealType.bytes)
    device = LocalStateValue(TealType.bytes)


emsights = Application("EMSights", state=EMSightsState())

@emsights.create
def create():
    return emsights.initialize_global_state()

@emsights.opt_in
def opt_in():
    return Approve()

# An address registers as a patient
@emsights.external
def registerAsPatient(name : abi.String, age: abi.Uint16, allergies: abi.String, medications: abi.String):
    return Seq(
        emsights.state.role.set(Bytes("P")),
        (consent := abi.String()).set("FFFF"),
        # (pt_info := PatientInfo()).set(name, age, allergies, medications, consent),
        # App.box_create(Txn.sender(), Int(10) )
        # emsights.state.patient_info[Txn.sender()].set(pt_info),
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

@emsights.external
def patientRegisterDevice(device : abi.Account):
    return Seq(
        Assert(emsights.state.role == Bytes("P")),
        emsights.state.device.set(device.address())
    )

# Register an account as a device
@emsights.external
def registerAsDevice():
    return emsights.state.role.set(Bytes("D"))

# @emsights.external
# def patientSetName(name : abi.String):
#     # contents = PatientInfo()
#     return Seq(
#         # Assert(emsights.state.patient_info[Txn.sender()].exists()),
#         # (pt_info := PatientInfo()).decode(emsights.state.patient_info[Txn.sender()].get()),
#         Assert(emsights.state.role == Bytes("Patient")),
#         emsights.state.name.set(name.get())
#     )

# @emsights.external
# def patientGetName(*, output : abi.String):
#     return Seq(
#         Assert(emsights.state.role == Bytes("Patient")),
#         (test := abi.String()).decode(emsights.state.name),
#         output.decode(emsights.state.role.get())
#     )

# @app.external(authorize=onlyPatient)
# def patientGetName(*, output : abi.DynamicArray[abi.String]):
#     ptKey = Concat(Txn.sender(), Bytes("p"))
#     return output.set(App.box_get(ptKey)[0])

# @app.external(authorize=onlyPatient)
# def patientSetAge(age : abi.Uint16):
#     ptKey = Concat(Txn.sender(), Bytes("p"))
#     return Seq(
#         contents := App.box_get(ptKey).value(),
#         App.box_put(ptKey,
#             PatientInfo(
#                 contents[0],
#                 age,
#                 contents[2],
#                 contents[3],
#                 contents[4]
#             )
#         )
#     )

# @app.external(authorize=onlyPatient)
# def patientGetAge(*, output : abi.Uint16):
#     ptKey = Concat(Txn.sender(), Bytes("p"))
#     return output.set(App.box_get(ptKey)[1])

# @app.external(authorize=onlyPatient)
# def patientSetAllergies(allergies : abi.DynamicArray[abi.String]):
#     ptKey = Concat(Txn.sender(), Bytes("p"))
#     return Seq(
#         contents := App.box_get(ptKey).value(),
#         App.box_put(ptKey,
#             PatientInfo(
#                 contents[0],
#                 contents[1],
#                 allergies,
#                 contents[3],
#                 contents[4]
#             )
#         )
#     )

# @app.external(authorize=onlyPatient)
# def patientGetAllergies(*, output : abi.DynamicArray[abi.String]):
#     ptKey = Concat(Txn.sender(), Bytes("p"))
#     return output.set(App.box_get(ptKey)[2])

# @app.external(authorize=onlyPatient)
# def patientSetMedications(medications : abi.DynamicArray[abi.String]):
#     ptKey = Concat(Txn.sender(), Bytes("p"))
#     return Seq(
#         contents := App.box_get(ptKey).value(),
#         App.box_put(ptKey,
#             PatientInfo(
#                 contents[0],
#                 contents[1],
#                 contents[2],
#                 medications,
#                 contents[4]
#             )
#         )
#     )

# @app.external(authorize=onlyPatient)
# def patientGetMedications(*, output : abi.DynamicArray[abi.String]):
#     ptKey = Concat(Txn.sender(), Bytes("p"))
#     return output.set(App.box_get(ptKey)[3])

if __name__ == "__main__":
    emsights.build().export("./artifacts")