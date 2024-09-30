from gradio_client import Client

client = Client("raannakasturi/orderSSL")
result = client.predict(
		i_domains="raannakasturi.eu.org",
		wildcard=True,
		email="raannakasturi@gmail.com",
		ca_server="Let's Encrypt (Testing)",
		key_type="ecc",
		key_size="4096",
		key_curve="SECP256R1",
		api_name="/gen_ssl"
)
print(result)