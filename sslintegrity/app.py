import sys
import requests
import gradio as gr
import json

def requestAPI(domain):
    url = f'https://ssl-checker.io/api/v1/check/{domain}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {e}'}
    
    # Process the data to match the desired output format
    data = response.json()
    result = data.get('result', {})

    formatted_data = {
        "Host": result.get("host", ""),
        "Status": data.get("status", ""),
        "Response Time": f"{data.get('response_time_sec', '0')}s",
        "Resolved IP": result.get("resolved_ip", ""),
        "Issued to": result.get("issued_to", ""),
        "Issued Organization": result.get("issued_o", None),
        "Issuer Country": result.get("issuer_c", ""),
        "Issuer CN": result.get("issuer_cn", ""),
        "Issuer Organization": result.get("issuer_o", ""),
        "Cert S/N": result.get("cert_sn", ""),
        "Cert SHA1": result.get("cert_sha1", ""),
        "Cert Algorithm": result.get("cert_alg", ""),
        "Cert Version": result.get("cert_ver", ""),
        "Cert SANs": result.get("cert_sans", ""),
        "Cert Expired": result.get("cert_exp", False),
        "Cert Valid": result.get("cert_valid", False),
        "Valid From": result.get("valid_from", ""),
        "Valid Until": result.get("valid_till", ""),
        "Validity Days": result.get("validity_days", 0),
        "Days Left": result.get("days_left", 0),
        "Valid Days to Expire": result.get("valid_days_to_expire", 0),
        "HSTS Header Enabled": result.get("hsts_header_enabled", False)
    }
    
    return json.dumps(formatted_data, indent=2)  # Format as pretty JSON

def app():
    with gr.Blocks(title="Project Gatekeeper - Get free SSL Certificates") as webui:
        domains_input = gr.Textbox(
            label="Enter Domains",
            placeholder="thenayankasturi.eu.org, dash.thenayankasturi.eu.org, www.thenayankasturi.eu.org",
            type="text",
            interactive=True
        )
        data = gr.TextArea(
            label="Data",
            placeholder="Data will be displayed here in JSON format",
            type="text",
            interactive=False
        )
        btn = gr.Button(value="Generate SSL Certificate")
        btn.click(requestAPI, inputs=domains_input, outputs=data)
    
    try:
        webui.queue(default_concurrency_limit=15).launch()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()
