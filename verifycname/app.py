import gradio as gr
from dns import resolver
from generateCNAMES import generate_cnames

def verify_cnames(i_domains, wildcard):
    cname_rec = []
    cname_value_expected = []
    cname_value_found = []
    cname_status = []
    cf_domain = "silerudaagartha.eu.org"
    
    # Generate CNAMEs based on input domains and cloudflare domain
    cname_recs, cname_values = generate_cnames(i_domains, cf_domain, wildcard)
    
    for rec, value in zip(cname_recs, cname_values):
        cname_record = None
        status = "Not Verified"  # Default status
        
        try:
            # Try resolving the CNAME record
            cname_answers = resolver.resolve(rec, 'CNAME')
            for answer in cname_answers:
                cname_record = answer.to_text().rstrip(".")  # Remove trailing dot
                
                # Check if the CNAME record matches the expected value
                if cname_record in value:
                    status = "Verified"
                    break  # Stop checking other answers once we find a valid one

        except Exception as e:
            # If there's an error, print it and leave status as "Not Verified"
            print(f"An error occurred while resolving {rec}: {e}")
        
        # Append results to lists
        cname_rec.append(rec)
        cname_value_expected.append(value)
        cname_value_found.append(cname_record or "None")
        cname_status.append(status)
    
    # Prepare table data for printing or returning
    table_data = []
    for record, expvalue, foundval, stat in zip(cname_rec, cname_value_expected, cname_value_found, cname_status):
        table_data.append([record, expvalue, foundval, stat])
    
    print(table_data)  # For debugging purposes
    return table_data

def app():
    with gr.Blocks(title="Verify CNAMES for Project Gatekeeper") as webui:
        with gr.Row():
            check_domains = gr.Textbox(label="Enter CNAME", placeholder="thenayankasturi.eu.org, dash.thenayankasturi.eu.org, www.thenayankasturi.eu.org", type="text", interactive=True)
            wildcard = gr.Checkbox(label="Wildcard", value=False)
            btn2 = gr.Button(value="Check CNAME Propagation")
        with gr.Row():
            data = gr.Dataframe(label="CNAME Records", headers=["CNAME", "Expected CNAME Value", "Found CNAME Value", "CNAME Status"], row_count=(1), col_count=(4))
        btn2.click(verify_cnames, inputs=[check_domains, wildcard], outputs=data)
    try:
        webui.queue(default_concurrency_limit=25).launch()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()
