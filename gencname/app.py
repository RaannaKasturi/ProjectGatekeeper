import gradio as gr
from generate_cnames import generate_cnames

def get_cnames(i_domains, wildcard=False):
    cf_domain = "silerudaagartha.eu.org"
    if wildcard:
        cname_recs, cname_values = generate_cnames(i_domains, cf_domain, wildcard)
    else:
        cname_recs, cname_values = generate_cnames(i_domains, cf_domain, wildcard)
    table_data = []
    for rec, value in zip(cname_recs, cname_values):
        table_data.append([rec, value])
    return table_data

def app():
    with gr.Blocks(title="Generate CNAMES for Project Gatekeeper") as webui:
        with gr.Row():
            cname_domains = gr.Textbox(label="Enter Domains", placeholder="thenayankasturi.eu.org, dash.thenayankasturi.eu.org, www.thenayankasturi.eu.org", type="text", interactive=True)
            wildcard = gr.Checkbox(label="Wildcard", value=False)
            btn = gr.Button(value="Generate CNAME Records & Values")
        with gr.Row():
            records = gr.Dataframe(label="CNAME Records", headers=["CNAME", "CNAME VALUE"], row_count=(1), col_count=(2))
        btn.click(get_cnames, inputs=[cname_domains, wildcard], outputs=records)
    try:
        webui.queue(default_concurrency_limit=25).launch()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()