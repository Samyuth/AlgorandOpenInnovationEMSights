from emsights import emsights, registerAsPatient, patientConsent, registerAsDevice, patientRegisterDevice, patientTriggerEmergency, dispatcherSelectResponder, responderQueryInformation
from beaker import sandbox, client, consts
from beaker.sandbox import SandboxAccount
from algosdk.encoding import decode_address
from algosdk import kmd, wallet, account

# app.build().export("./artifacts")
emsights.build().export("./artifacts")

# print(sandbox.kmd.get_accounts())

accounts = sandbox.kmd.get_accounts()
patient = accounts[0]
device = accounts[1]
dispatcher = accounts[2]
# emt = accounts[3]

pt_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=emsights,
    sender=patient.address,
    signer=patient.signer,
)

# pt_client.fund(consts.algo * 1500)

pt_client.create(sender=dispatcher.address, signer=dispatcher.signer)

pt_client.opt_in()
pt_client.opt_in(sender=device.address, signer=device.signer)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

address = patient.address
pk = decode_address(address)

pt_client.call(
    registerAsPatient,
    name = "Samyuth S Sagi",
    age = 21,
    allergies = "[dust]",
    medications = "",
    # boxes=[tuple([pt_client.app_id, decode_address(patient.address)])]
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

# pt_client.call(
#     registerAsDevice,
#     sender=device.address,
#     signer=device.signer
# )

# print(pt_client.get_global_state())
# print(pt_client.get_local_state(patient.address))
# print(pt_client.get_local_state(device.address))
# print()

# pt_client.call(
#     patientRegisterDevice,
#     device=device.address
# )

# print(pt_client.get_global_state())
# print(pt_client.get_local_state(patient.address))
# print(pt_client.get_local_state(device.address))
# print()

pt_client.call(
    patientConsent,
    consent="TTTF"
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()


pt_client.call(
    patientTriggerEmergency
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

pt_client.call(
    patientTriggerEmergency
)

print(pt_client.get_global_state()['emergency_queue'][0:64] == pt_client.get_global_state()['emergency_queue'][64:])
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

pt_client.call(
    dispatcherSelectResponder,
    responder=dispatcher.address,
    patient=patient.address,
    sender=dispatcher.address,
    signer=dispatcher.signer
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

rt = pt_client.call(
    responderQueryInformation,
    patient=patient.address,
    field="allergies",
    sender=dispatcher.address,
    signer=dispatcher.signer
).return_value

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print(rt)
