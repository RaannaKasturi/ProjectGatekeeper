import gradio as gr
from matcher import fetch_data

def get_status(csrpvt, cert):
    status = fetch_data(csrpvt, cert)
    return status

app = gr.Interface(fn=fetch_data, inputs=["textbox", "textbox"], outputs="textbox")
app.launch()