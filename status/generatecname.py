from gradio_client import Client

client = Client("raannakasturi/gencname")
result = client.predict(
		i_domains="thenayankasturi.eu.org, www.thenayankasturi.eu.org",
		wildcard=False,
		api_name="/get_cnames"
)
print(result['data'])