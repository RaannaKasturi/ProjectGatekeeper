from privcsr import gen_pvt, gen_csr, gen_pvt_csr
import gradio as gr

def update_key_options(key_type):
    if key_type == "rsa":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)
    
def privcsr(domains_input, email, key_type, key_size=None, key_curve=None):
    domains = domains_input.split(",")
    if key_type.lower() == 'rsa':
        private_key, csr = gen_pvt_csr(domains, email, key_type, key_size=int(key_size))
    else:
        private_key, csr = gen_pvt_csr(domains, email, key_type, key_curve=key_curve)
    return private_key.decode(), csr.decode()

def app():
    with gr.Blocks(title="Project Gatekeeper - Get free SSL Certificates") as webui:
        with gr.Row():
            with gr.Column():
                domains_input = gr.Textbox(label="Enter Domains", placeholder="thenayankasturi.eu.org, *.thenayankasturi.eu.org", type="text", interactive=True, value="thenayankasturi.eu.org, *.thenayankasturi.eu.org")
                email = gr.Textbox(label="Enter Email", placeholder="admin@thenayankasturi.eu.org", type="text", interactive=True, value="admin@gmail.com")
        with gr.Row():
            key_type = gr.Radio(label="Select SSL key type", choices=["rsa", "ecc"], interactive=True, value='ecc')
            key_size_dropdown = gr.Dropdown(label="Select Key Size", choices=['2048', '4096'], value='4096', visible=False)  # Initially visible
            key_curve_dropdown = gr.Dropdown(label="Select Key Curve", choices=['SECP256R1', 'SECP384R1'], value='SECP256R1', visible=True)  # Initially hidden
        key_type.change(fn=update_key_options, inputs=key_type, outputs=[key_size_dropdown, key_curve_dropdown])
        btn = gr.Button(value="Generate SSL Certificate")
        with gr.Row():
            with gr.Column():
                pvt = gr.Textbox(label="Your Private Key", placeholder="Your Private Key will appear here, after successful SSL generation", type="text", interactive=False, show_copy_button=True, lines=10, max_lines=10)
            with gr.Column():
                csr = gr.Textbox(label="Your CSR", placeholder="Your CSR will appear here, after successful SSL generation", type="text", interactive=False, show_copy_button=True, lines=10, max_lines=10)
        btn.click(privcsr, inputs=[domains_input, email, key_type, key_size_dropdown, key_curve_dropdown], outputs=[pvt, csr])
    try:
        webui.queue(default_concurrency_limit=15).launch()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()