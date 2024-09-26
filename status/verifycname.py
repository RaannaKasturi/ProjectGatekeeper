from gradio_client import Client

client = Client("raannakasturi/verifycname")
result = client.predict(
		i_domains="thenayankasturi.eu.org, dash.thenayankasturi.eu.org",
		wildcard=False,
		api_name="/verify_cnames"
)
print(result)