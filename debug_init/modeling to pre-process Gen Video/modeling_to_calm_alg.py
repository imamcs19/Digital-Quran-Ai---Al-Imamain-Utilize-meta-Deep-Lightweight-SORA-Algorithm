## Model 1 utilize surah makkiyah
## Model 2 utilize surah madaniyah
## Model 3 utilize surah 'makiyah_dan_madaniyah' + 'turun_diantara_makiyah_dan_madaniyah'
## Model 4 As Baseline or Grouth Truth utilize all Surah

import json
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np

# Konfigurasi variabel global
n_input = 475
n_hidden1 = int(n_input * 2.0)
n_hidden2 = int(n_hidden1 * 0.75)
n_output = 114

# Definisi model ELM dengan dua hidden layers untuk regresi
class ELMRegression(nn.Module):
    def __init__(self, n_input, n_hidden1, n_hidden2, n_output):
        super(ELMRegression, self).__init__()
        self.hidden1 = nn.Linear(n_input, n_hidden1)
        self.hidden2 = nn.Linear(n_hidden1, n_hidden2)
        self.output = nn.Linear(n_hidden2, n_output)

    def forward(self, x):
        x = torch.sigmoid(self.hidden1(x))
        x = torch.sigmoid(self.hidden2(x))
        return self.output(x)

# Fungsi menyimpan model dalam format JSON
def save_model_json(model, file_path):
    model_params = {
        "hidden1_weights": model.hidden1.weight.detach().numpy().tolist(),
        "hidden1_bias": model.hidden1.bias.detach().numpy().tolist(),
        "hidden2_weights": model.hidden2.weight.detach().numpy().tolist(),
        "hidden2_bias": model.hidden2.bias.detach().numpy().tolist(),
        "output_weights": model.output.weight.detach().numpy().tolist(),
        "output_bias": model.output.bias.detach().numpy().tolist()
    }
    with open(file_path, 'w') as json_file:
        json.dump(model_params, json_file)
    print(f"Model saved as JSON at {file_path}")

# Fungsi menyimpan loss per epoch dalam JSON
def save_loss_json(loss_per_epoch, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(loss_per_epoch, json_file)
    print(f"Loss per epoch saved as JSON at {file_path}")

# Fungsi untuk mem-plot dan menyimpan hasil training (loss per epoch)
def plot_loss(loss_per_epoch, sheet_name):
    epochs = list(range(1, len(loss_per_epoch) + 1))
    plt.figure()
    plt.plot(epochs, loss_per_epoch, label='Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title(f'Training Loss per Epoch for {sheet_name}')
    plt.legend()
    plt.savefig(f'output_model/loss_plot_{sheet_name}.png')
    plt.savefig(f'output_model/loss_plot_{sheet_name}.pdf')
    print(f"Loss plot saved as PNG and PDF for {sheet_name}")
    plt.close()

# Fungsi untuk memuat data dan melakukan ELM regresi
def perform_elm_regression(file_path, sheets, epochs=100):
    excel_file = pd.ExcelFile(file_path)
    for sheet_name in sheets:
        print(f"Processing sheet: {sheet_name}")
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])

        X = df.iloc[:, :n_input].values
        y = df.iloc[:, n_input:n_input + n_output].values
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)

        elm_model = ELMRegression(n_input, n_hidden1, n_hidden2, n_output)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(elm_model.parameters(), lr=0.01)
        loss_per_epoch = []

        elm_model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = elm_model(X_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()
            loss_per_epoch.append(loss.item())

        save_model_json(elm_model, f'output_model/model_{sheet_name}.json')
        save_loss_json(loss_per_epoch, f'output_model/loss_{sheet_name}.json')
        plot_loss(loss_per_epoch, sheet_name)
        print(f"Final Loss for {sheet_name}: {loss_per_epoch[-1]}")

# Fungsi membuat sheet gabungan dari beberapa sheet
def create_combined_sheet(file_path, sheets, combined_sheet_name="CombinedSheet"):
    excel_file = pd.ExcelFile(file_path)
    combined_df = pd.DataFrame()

    for sheet_name in sheets:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        combined_df.to_excel(writer, sheet_name=combined_sheet_name, index=False)
    
    print(f"Combined sheet '{combined_sheet_name}' created/overwritten in {file_path}")

# Fungsi meload model dari file JSON
def load_model_json(file_path, model):
    with open(file_path, 'r') as json_file:
        model_params = json.load(json_file)
    
    model.hidden1.weight.data = torch.FloatTensor(model_params['hidden1_weights'])
    model.hidden1.bias.data = torch.FloatTensor(model_params['hidden1_bias'])
    model.hidden2.weight.data = torch.FloatTensor(model_params['hidden2_weights'])
    model.hidden2.bias.data = torch.FloatTensor(model_params['hidden2_bias'])
    model.output.weight.data = torch.FloatTensor(model_params['output_weights'])
    model.output.bias.data = torch.FloatTensor(model_params['output_bias'])
    print(f"Model loaded from {file_path}")

# Fungsi menguji model dengan dataset
def test_model(model, X_tensor, y_true):
    model.eval()
    with torch.no_grad():
        predictions = model(X_tensor)
        mse_loss = nn.MSELoss()(predictions, torch.FloatTensor(y_true))
        print(f'Testing Loss: {mse_loss.item()}')

# Fungsi untuk memuat dan menguji semua model dari setiap sheet
def load_and_test_all_models(file_path, sheets):
    excel_file = pd.ExcelFile(file_path)
    for sheet_name in sheets:
        print(f"Testing model for sheet: {sheet_name}")
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        X = df.iloc[:, :n_input].values
        y = df.iloc[:, n_input:n_input + n_output].values

        elm_model = ELMRegression(n_input, n_hidden1, n_hidden2, n_output)
        load_model_json(f'output_model/model_{sheet_name}.json', elm_model)
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)

        test_model(elm_model, X_tensor, y_tensor)

# Eksekusi regresi pada file Excel
file_path = 'dataset/quran_json_ekstrak/dataset_translations-top_15_to_model_v1.xlsx'
sheets = ['list_model_sheet1', 'list_model_sheet2', 'list_model_sheet3', 'list_model_comb_all_unique']
perform_elm_regression(file_path, sheets, epochs=500)
