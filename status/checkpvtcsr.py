from gradio_client import Client

client = Client("raannakasturi/generate-pvt-csr")
result = client.predict(
		domains_input="thenayankasturi.eu.org, *.thenayankasturi.eu.org",
		email="admin@gmail.com",
		key_type="ecc",
		key_size="4096",
		key_curve="SECP256R1",
		api_name="/privcsr"
)
print(result)