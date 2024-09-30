from gradio_client import Client

client = Client("raannakasturi/verifycname")
result = client.predict(
		i_domains="thenayankasturi.eu.org, *.thenayankasturi.eu.org",
		wildcard=True,
		api_name="/verify_cnames"
)
print(result)