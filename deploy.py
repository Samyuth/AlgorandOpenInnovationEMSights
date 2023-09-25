from emsights import (
    emsights,
    registerAsPatient,
    patientConsent,
    registerAsDevice,
    patientRegisterDevice,
    patientTriggerEmergency,
    dispatcherSelectResponder, 
    responderQueryInformation,
    responderTransferCare
)

from beaker import localnet, client
from algosdk.encoding import decode_address
from algosdk import kmd, wallet, account

emsights.build().export("./artifacts")

# get localnet accounts
accounts = localnet.kmd.get_accounts()
patient = accounts[0]
device = accounts[1]
dispatcher = accounts[2]
emt = accounts[3]
physician = accounts[4]

pt_client = client.ApplicationClient(
    client=localnet.get_algod_client(),
    app=emsights,
    sender=patient.address,
    signer=patient.signer,
)

# dispatcher creates the emsights contract
pt_client.create(sender=dispatcher.address, signer=dispatcher.signer)

# patient opts in to the contract and so does the device
pt_client.opt_in()
pt_client.opt_in(sender=device.address, signer=device.signer)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

address = patient.address
pk = decode_address(address)

# Call register patient function
pt_client.call(
    registerAsPatient,
    name = "Samyuth S Sagi",
    age = 21,
    allergies = "[dust]",
    medications = ""
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

# register an account as a device
# pt_client.call(
#     registerAsDevice,
#     sender=device.address,
#     signer=device.signer
# )

# print(pt_client.get_global_state())
# print(pt_client.get_local_state(patient.address))
# print(pt_client.get_local_state(device.address))
# print()

# get the patient to register the device
# pt_client.call(
#     patientRegisterDevice,
#     device=device.address
# )

# print(pt_client.get_global_state())
# print(pt_client.get_local_state(patient.address))
# print(pt_client.get_local_state(device.address))
# print()

# patient consents to information they are willing to release
pt_client.call(
    patientConsent,
    consent="TTTF"
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()


# a patient has an emergency
pt_client.call(
    patientTriggerEmergency
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

# patient once again triggers an emergency
pt_client.call(
    patientTriggerEmergency
)

print(pt_client.get_global_state()['emergency_queue'][0:64] == pt_client.get_global_state()['emergency_queue'][64:])
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

# the dispatcher address chooses a responder
pt_client.call(
    dispatcherSelectResponder,
    responder=emt.address,
    patient=patient.address,
    sender=dispatcher.address,
    signer=dispatcher.signer
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

# responder can now view specific information
rt = pt_client.call(
    responderQueryInformation,
    patient=patient.address,
    field="allergies",
    sender=emt.address,
    signer=emt.signer
).return_value

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print(rt)
print()

# responder transfers care to physician
pt_client.call(
    responderTransferCare,
    patient=patient.address,
    reciever=physician.address,
    sender=emt.address,
    signer=emt.signer
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

# # emt can no longer view patient information
# rt = pt_client.call(
#     responderQueryInformation,
#     patient=patient.address,
#     field="allergies",
#     sender=emt.address,
#     signer=emt.signer
# ).return_value

# physician can now view patient information
rt = pt_client.call(
    responderQueryInformation,
    patient=patient.address,
    field="allergies",
    sender=physician.address,
    signer=physician.signer
).return_value

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print(rt)
print()
