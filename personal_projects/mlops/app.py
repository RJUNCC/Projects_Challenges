import os
import joblib
import gradio as gr
import pandas as pd

price_predictor = joblib.load('model-v3.joblib')

carat_input = gr.Number(label="Carat")

shape_input = gr.Dropdown(
    ['Round', 'Princess', 'Emerald', 'Asscher', 'Cushion', 'Radiant', 'Oval', 'Pear', 'Marquise'],
    label="Shape"
)

cut_input = gr.Dropdown(
    ['Ideal', 'Premium', 'Very Good', 'Good', 'Fair'],
    label="Cut"
)

color_input = gr.Dropdown(
    ["D", "E", "F", "G", "H", "I", "J"],
    label="Color"
)

clarity_input = gr.Dropdown(
    ["IF", "VVs1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I2"],
    label="Clarity"
)

report_input = gr.Dropdown(['GIA', 'IGI', 'HRD', 'AGS'],
                           label="Type")

# hf_token = os.environ["HF_TOKEN"]
# hr_writer = gr.HuggingFaceDatasetSaver(hf_token, "diamond-price-predictor-logs")

model_output = gr.Label(label="Predicted Price (USD)")

def predict_price(carat, shape, cut, color, clarity, report, type):
    sample = {
        'carat': carat,
        'shape': shape,
        'cut': cut,
        'color': color,
        'clarity': clarity,
        'report': report,
        'type': type
    }

    data_point = pd.DataFrame([sample])
    prediction = price_predictor.predict(data_point)

demo = gr.Interface(
    fn=predict_price,
    inputs=[carat_input, shape_input, cut_input, color_input, clarity_input, report_input, type_input],
    outputs=model_output,
    theme=gr.themes.Soft(),
    title="Diamond Price Predictor",
    description="This API allows you to predict the price of a diamond given its attributes",
    allow_flagging="auto",
    # flagging_callback=hf_writer,
    concurrency_limit=8
)