import gradio as gr
import pickle
import pandas as pd
import numpy as np

# Загрузите модель из файла pickle
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)


# Определите функцию для предсказания
def predict_rul_from_file(file):
    if file is None:
        return "No file uploaded"

    df = pd.read_excel(file.name)

    required_columns = ['setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9',
                        's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21']

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return f"File is missing required columns. Missing columns are: {missing_columns}"

    features = df[required_columns].values
    predictions = model.predict(features)

    # Обработка отрицательных значений
    predictions = np.maximum(predictions, 0)

    df['Predicted RUL'] = predictions

    result_file = "predictions.xlsx"
    df.to_excel(result_file, index=False)

    return result_file


interface = gr.Interface(
    fn=predict_rul_from_file,
    inputs=gr.File(label="Upload Excel File"),
    outputs="file",
    title="RUL Prediction from Excel",
    description="Upload an Excel file with the required columns to get the predicted Remaining Useful Life (RUL). The results will be saved in an Excel file with an index column."
)

if __name__ == "__main__":
    interface.launch()
