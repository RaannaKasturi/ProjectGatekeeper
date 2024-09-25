import json
import gradio as gr
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from decode import decode_ssl_certificate

def decode(cert) -> dict:
    cert = cert.encode()
    ssl_out = {}
    try:
        decoded_cert = x509.load_pem_x509_certificate(cert, default_backend())
        if decoded_cert:
            status = "Success"
            message = "Certificate decoded successfully."
            decoded_data = decode_ssl_certificate(decoded_cert)
            data = {
                "status": status,
                "message": message,
                "data": decoded_data
            }
            ssl_out = json.dumps(data, indent = 4)
        else:
            data = {
                "status": status,
                "message": message,
                "data": None
            }
            ssl_out = json.dumps(data, indent = 4)
    except Exception as e:
        status = "Failed"
        message = "Failed to decode certificate. Please make sure you have uploaded a valid certificate file."
        data = {
                "status": status,
                "message": message,
                "data": e
            }
        ssl_out = json.dumps(data, indent = 4)
    return ssl_out

def app():
    with gr.Blocks(title="Project Gatekeeper - Get free SSL Certificates") as webui:
        with gr.Row():
            ssl = gr.Textbox(label="Enter Domains", type="text", interactive=True)
        with gr.Row():
            decoded_data = gr.Textbox(label="Enter Domains", type="text", interactive=False, show_copy_button=True)
        btn = gr.Button(value="Generate SSL Certificate")
        btn.click(decode, inputs=ssl, outputs=decoded_data)
    try:
        webui.queue(default_concurrency_limit=15).launch()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()