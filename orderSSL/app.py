import os
import sys
import gradio as gr
from main import main

def gen_ssl(i_domains, wildcard, email, ca_server, key_type, key_size=None, key_curve=None):
    if key_type == "rsa":
        key_curve = None
    elif key_type == "ecc":
        key_size = None
    else:
        key_curve = None
    if key_size is not None:
        key_size = int(key_size)
    print(f"Domains {i_domains}")
    print(f"wildcard {wildcard}")
    print(f"email {email}")
    print(f"ca server {ca_server}")
    print(f"keytype {key_type}")
    print(f"keysize {key_size}")
    print(f"keycurve {key_curve}")
    pvt, csr, cert, email_status = main(i_domains, wildcard, email, ca_server, key_type, key_size, key_curve)
    print("SSL Certificate generated successfully")
    try:
        return pvt.decode('utf-8'), csr.decode('utf-8'), cert.decode('utf-8'), email_status
    except:
        return pvt, csr, cert, email_status

def update_key_options(key_type):
    if key_type == "rsa":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)

def update_ca_server(wildcard: bool):
    if wildcard == False:
        return gr.update(choices=["Let's Encrypt (Testing)","Let's Encrypt", "Buypass (Testing)", "Buypass", "ZeroSSL", "Google (Testing)","Google", "SSL.com"], value="Let's Encrypt (Testing)")
    else:
        return gr.update(choices=["Let's Encrypt (Testing)","Let's Encrypt", "ZeroSSL", "Google (Testing)","Google", "SSL.com"], value="Let's Encrypt")

def update_buypass_options(ca_server):
    if ca_server == "Buypass (Testing)" or ca_server == "Buypass":
        return gr.update(choices=['SECP256R1'])
    else:
        return gr.update(choices=['SECP256R1', 'SECP384R1'])

def app():
    with gr.Blocks(title="Project Gatekeeper - Get free SSL Certificates") as webui:
        with gr.Row():
            with gr.Column():
                domains_input = gr.Textbox(label="Enter Domains", placeholder="thenayankasturi.eu.org, dash.thenayankasturi.eu.org, www.thenayankasturi.eu.org", type="text", interactive=True)
                wildcard = gr.Checkbox(label="Wildcard SSL", interactive=True, value=False)
            email_input = gr.Textbox(label="Enter your Email ID", placeholder="nayankasturi@gmail.com", type="text", interactive=True)
        with gr.Row():
            ca_server = gr.Dropdown(label="Select Certificate Authority", choices=["Let's Encrypt (Testing)","Let's Encrypt", "Google (Testing)","Google", "Buypass (Testing)", "Buypass", "ZeroSSL", "SSL.com"], interactive=True, value="Let's Encrypt (Testing)")
            key_type = gr.Radio(label="Select SSL key type", choices=["rsa", "ecc"], interactive=True, value='ecc')
            key_size_dropdown = gr.Dropdown(label="Select Key Size", choices=['2048', '4096'], value='4096', visible=False)  # Initially visible
            key_curve_dropdown = gr.Dropdown(label="Select Key Curve", choices=['SECP256R1', 'SECP384R1'], value='SECP256R1', visible=True)  # Initially hidden
        ca_server.change(fn=update_buypass_options, inputs=ca_server, outputs=key_curve_dropdown)
        key_type.change(fn=update_key_options, inputs=key_type, outputs=[key_size_dropdown, key_curve_dropdown])
        wildcard.change(fn=update_ca_server, inputs=wildcard, outputs=ca_server)
        btn = gr.Button(value="Generate SSL Certificate")
        with gr.Row():
            with gr.Column():
                pvt = gr.Textbox(label="Your Private Key", placeholder="Your Private Key will appear here, after successful SSL generation", type="text", interactive=False, show_copy_button=True, lines=10, max_lines=10)
            with gr.Column():
                csr = gr.Textbox(label="Your CSR", placeholder="Your CSR will appear here, after successful SSL generation", type="text", interactive=False, show_copy_button=True, lines=10, max_lines=10)
            with gr.Column():
                crt = gr.Textbox(label="Your SSL Certificate", placeholder="Your SSL Certificate will appear here, after successful SSL generation", type="text", interactive=False, show_copy_button=True, lines=10, max_lines=10)
        email_status = gr.Textbox(label="Email Status", placeholder="Email status will appear here, after sending email", type="text", interactive=False)
        btn.click(gen_ssl, inputs=[domains_input, wildcard, email_input, ca_server, key_type, key_size_dropdown, key_curve_dropdown], outputs=[pvt, csr, crt, email_status])
    try:
        webui.queue(default_concurrency_limit=15).launch()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()
