from app import app, hello
from emsights import emsights, registerAsPatient, patientConsent, registerAsDevice
from beaker import sandbox, client, consts
from algosdk.encoding import decode_address

# app.build().export("./artifacts")
emsights.build().export("./artifacts")

accounts = sandbox.kmd.get_accounts()
patient = accounts[0]
device = accounts[1]

pt_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=emsights,
    sender=patient.address,
    signer=patient.signer,
)

# pt_client.fund(consts.algo * 1500)

pt_client.create()

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

pt_client.call(
    registerAsDevice,
    sender=device.address,
    signer=device.signer
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

pt_client.call(
    patientConsent,
    consent="TTTF"
)

print(pt_client.get_global_state())
print(pt_client.get_local_state(patient.address))
print(pt_client.get_local_state(device.address))
print()

# print(return_value)
