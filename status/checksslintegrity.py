from gradio_client import Client

client = Client("raannakasturi/sslintegrity")
result = client.predict(
		domain="nayankasturi.eu.org",
		api_name="/requestAPI"
)
print(result)
