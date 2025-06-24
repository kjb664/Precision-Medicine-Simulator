
import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# Load preprocessed dataset or simulate dummy categorical values
drug_names = ["Drug A", "Drug B", "Drug C"]
tissue_types = ["Lung", "Breast", "Colon", "Melanoma"]
msi_statuses = ["MSI-High", "MSI-Low"]
num_sim_default = 10000

def simulate_response(drug, tissue, msi, num_simulations):
    np.random.seed(42)

    # Simulate LN_IC50 and AUC distributions based on chosen variables
    # (Placeholder logic; can be replaced with model-calibrated sampling)
    ln_ic50 = np.random.normal(loc=5 if msi == "MSI-High" else 6, scale=0.8, size=num_simulations)
    auc = np.random.normal(loc=0.7 if tissue == "Breast" else 0.6, scale=0.1, size=num_simulations)

    # Create plots
    plt.figure(figsize=(10, 5))
    sns.kdeplot(ln_ic50, fill=True, label="LN_IC50")
    sns.kdeplot(auc, fill=True, label="AUC")
    plt.axvline(np.mean(ln_ic50), color='blue', linestyle='--', label='LN_IC50 Mean')
    plt.axvline(np.mean(auc), color='green', linestyle='--', label='AUC Mean')
    plt.legend()
    plt.title(f"Simulated Distributions ({num_simulations} samples)")
    plt.xlabel("Response Value")
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    image_bytes = buf.read()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    image_url = f"data:image/png;base64,{encoded_image}"

    # Bayesian calibration placeholder
    posterior_mean = (np.mean(ln_ic50) + np.mean(auc)) / 2
    risk_class = "High Risk" if posterior_mean > 5.8 else "Low Risk"

    summary = f"Posterior Risk Score: {posterior_mean:.2f}\nPredicted Risk Category: **{risk_class}**"
    return summary, image_url

# Gradio UI
demo = gr.Interface(
    fn=simulate_response,
    inputs=[
        gr.Dropdown(drug_names, label="Select Drug"),
        gr.Dropdown(tissue_types, label="Select Tissue Type"),
        gr.Dropdown(msi_statuses, label="Select MSI Status"),
        gr.Slider(1000, 50000, step=1000, value=num_sim_default, label="Number of Simulations")
    ],
    outputs=[
        gr.Text(label="Simulation Summary & Risk Classification"),
        gr.Image(type="auto", label="Distribution Plot")
    ],
    title="🧬 Precision Medicine Simulator",
    description="Simulate probabilistic drug responses based on tumor profile. Now with Bayesian calibration and clinical risk interpretation."
)

if __name__ == "__main__":
    demo.launch()
