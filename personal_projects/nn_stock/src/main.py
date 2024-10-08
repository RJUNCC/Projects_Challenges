#%%
from config import Config
from data_prep import Normalizer, Prep
from time_series import TimeSeriesDataset
from lstm import LSTMModel

import matplotlib.pyplot as plt
import numpy as np

import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import seaborn as sns
import pandas as pd
from datetime import datetime

#%%
cfg = Config("MCFT")
config = cfg.config
data, data_date, data_close_price, num_data_points, display_date_range = cfg.download_data()

#%%
scaler = Normalizer()
normalized_data_close_price = scaler.fit_transform(data_close_price)

prep = Prep()
data_x, data_x_unseen = prep.prepare_data_x(normalized_data_close_price, window_size=config['data']['window_size'])
data_y = prep.prepare_data_y(normalized_data_close_price, window_size=config["data"]["window_size"])

#%% split dataset
split_index = int(data_y.shape[0]*config["data"]["train_split_size"])
data_x_train = data_x[:split_index]
data_x_val = data_x[split_index:]
data_y_train = data_y[:split_index]
data_y_val = data_y[split_index:]

#%% prepare data for plotting
to_plot_data_y_train = np.zeros(num_data_points)
to_plot_data_y_val = np.zeros(num_data_points)

to_plot_data_y_train[config["data"]["window_size"]:split_index+config["data"]["window_size"]] = scaler.inverse_transform(data_y_train)
to_plot_data_y_val[split_index+config["data"]["window_size"]:] = scaler.inverse_transform(data_y_val)

to_plot_data_y_train = np.where(to_plot_data_y_train == 0, None, to_plot_data_y_train)
to_plot_data_y_val = np.where(to_plot_data_y_val == 0, None, to_plot_data_y_val)


#%%
sns.lineplot(data=data, x=data_date, y=data_close_price)
# plt.xticks(x, xticks, rotation=90)
plt.xticks(rotation=90)
plt.show()

#%%
sns.lineplot(data=data, x=data_date, y=to_plot_data_y_train)
plt.xticks(rotation=90)
plt.show()

#%%
sns.lineplot(data=data, x=data_date, y=to_plot_data_y_val)
plt.xticks(rotation=90)
plt.show()

#%%
dataset_train = TimeSeriesDataset(data_x_train, data_y_train)
dataset_val = TimeSeriesDataset(data_x_val, data_y_val)

print("Train data shape", dataset_train.x.shape, dataset_train.y.shape)
print("Validation data shape", dataset_val.x.shape, dataset_val.y.shape)

train_dataloader = DataLoader(dataset_train, batch_size=config["training"]["batch_size"], shuffle=True)
val_dataloader = DataLoader(dataset_val, batch_size=config["training"]["batch_size"], shuffle=True)

#%%
def run_epoch(dataloader, is_training=False):
        epoch_loss = 0

        if is_training:
            model.train()
        else:
            model.eval()

        for idx, (x, y) in enumerate(dataloader):
            if is_training:
                optimizer.zero_grad()

            batchsize = x.shape[0]

            x = x.to(config["training"]["device"])
            y = y.to(config["training"]["device"])

            out = model(x)
            loss = criterion(out.contiguous(), y.contiguous())

            if is_training:
                loss.backward()
                optimizer.step()

            epoch_loss += (loss.detach().item() / batchsize)

        lr = scheduler.get_last_lr()[0]

        return epoch_loss, lr

#%%
train_dataloader = DataLoader(dataset_train, batch_size=config["training"]["batch_size"], shuffle=True)
val_dataloader = DataLoader(dataset_val, batch_size=config["training"]["batch_size"], shuffle=True)

model = LSTMModel(input_size=config["model"]["input_size"], hidden_layer_size=config["model"]["lstm_size"], num_layers=config["model"]["num_lstm_layers"], output_size=1, dropout=config["model"]["dropout"])
model = model.to(config["training"]["device"])

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=config["training"]["learning_rate"], betas=(0.9, 0.98), eps=1e-9)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=config["training"]["scheduler_step_size"], gamma=0.1)

for epoch in range(config["training"]["num_epoch"]):
    loss_train, lr_train = run_epoch(train_dataloader, is_training=True)
    loss_val, lr_val = run_epoch(val_dataloader)
    scheduler.step()
    
    print('Epoch[{}/{}] | loss train:{:.6f}, test:{:.6f} | lr:{:.6f}'.format(epoch+1, config["training"]["num_epoch"], loss_train, loss_val, lr_train))
    

#%% here we re-initialize dataloader so the data doesn't shuffled, so we can plot the values by date

train_dataloader = DataLoader(dataset_train, batch_size=config["training"]["batch_size"], shuffle=False)
val_dataloader = DataLoader(dataset_val, batch_size=config["training"]["batch_size"], shuffle=False)

model.eval()

#%% predict on the training data, to see how well the model managed to learn and memorize

predicted_train = np.array([])

for idx, (x, y) in enumerate(train_dataloader):
    x = x.to(config["training"]["device"])
    out = model(x)
    out = out.cpu().detach().numpy()
    predicted_train = np.concatenate((predicted_train, out))

#%% predict on the validation data, to see how the model does

predicted_val = np.array([])

for idx, (x, y) in enumerate(val_dataloader):
    x = x.to(config["training"]["device"])
    out = model(x)
    out = out.cpu().detach().numpy()
    predicted_val = np.concatenate((predicted_val, out))

#%% prepare data for plotting

to_plot_data_y_train_pred = np.zeros(num_data_points)
to_plot_data_y_val_pred = np.zeros(num_data_points)

to_plot_data_y_train_pred[config["data"]["window_size"]:split_index+config["data"]["window_size"]] = scaler.inverse_transform(predicted_train)
to_plot_data_y_val_pred[split_index+config["data"]["window_size"]:] = scaler.inverse_transform(predicted_val)

to_plot_data_y_train_pred = np.where(to_plot_data_y_train_pred == 0, None, to_plot_data_y_train_pred)
to_plot_data_y_val_pred = np.where(to_plot_data_y_val_pred == 0, None, to_plot_data_y_val_pred)


#%%
sns.lineplot(x=data_date, y=data_close_price, label="Actual")
sns.lineplot(x=data_date, y=to_plot_data_y_train_pred, label="Predicted prices (train)")
sns.lineplot(x=data_date, y=to_plot_data_y_val_pred, label="Predicted prices (validation)")
plt.xticks(rotation=90)
plt.legend()
plt.show()

#%% prepare data for plotting the zoomed in view of the predicted prices (on validation set) vs. actual prices
to_plot_data_y_val_subset = scaler.inverse_transform(data_y_val)
to_plot_predicted_val = scaler.inverse_transform(predicted_val)
to_plot_data_date = data_date[split_index+config["data"]["window_size"]:]


#%%
sns.lineplot(x=to_plot_data_date, y=to_plot_data_y_val_subset, label="Actual prices")
sns.lineplot(x=to_plot_data_date, y=to_plot_predicted_val, label="Predicted prices (validation)")
plt.xticks(rotation=90)
plt.legend()
plt.show()

#%% predict the closing price of the next trading day
model.eval()

x = torch.tensor(data_x_unseen).float().to(config["training"]["device"]).unsqueeze(0).unsqueeze(2) # this is the data type and shape required, [batch, sequence, feature]
prediction = model(x)
prediction = prediction.cpu().detach().numpy()

# prepare plots

plot_range = 10
to_plot_data_y_val = np.zeros(plot_range)
to_plot_data_y_val_pred = np.zeros(plot_range)
to_plot_data_y_test_pred = np.zeros(plot_range)

to_plot_data_y_val[:plot_range-1] = scaler.inverse_transform(data_y_val)[-plot_range+1:]
to_plot_data_y_val_pred[:plot_range-1] = scaler.inverse_transform(predicted_val)[-plot_range+1:]

to_plot_data_y_test_pred[plot_range-1] = scaler.inverse_transform(prediction)

to_plot_data_y_val = np.where(to_plot_data_y_val == 0, None, to_plot_data_y_val)
to_plot_data_y_val_pred = np.where(to_plot_data_y_val_pred == 0, None, to_plot_data_y_val_pred)
to_plot_data_y_test_pred = np.where(to_plot_data_y_test_pred == 0, None, to_plot_data_y_test_pred)

#%% plot
data_date_ls = data_date.dt.strftime("%Y-%m-%d")
# plot_date_test = data_date.tolist()[-plot_range+1:]
plot_date_test = data_date_ls.tolist()[-plot_range+1:]
plot_date_test.append("tomorrow")


#%%
# sns.lineplot(x=plot_date_test, y=to_plot_data_y_val, label="Actual prices")
# sns.lineplot(x=plot_date_test, y=to_plot_data_y_val_pred, label="Past predicted prices")
# sns.lineplot(x=plot_date_test, y=to_plot_data_y_test_pred, label="Predicted price for next days", markers=True)
# plt.legend()
# plt.xticks(rotation=90)
# plt.show()


#%%
fig = plt.figure(figsize=(25, 15), dpi=80)
fig.patch.set_facecolor((1.0, 1.0, 1.0))
plt.plot(plot_date_test, to_plot_data_y_val, label="Actual prices", marker=".", markersize=10, color=config["plots"]["color_actual"])
plt.plot(plot_date_test, to_plot_data_y_val_pred, label="Past predicted prices", marker=".", markersize=10, color=config["plots"]["color_pred_val"])
plt.plot(plot_date_test, to_plot_data_y_test_pred, label="Predicted price for next day", marker=".", markersize=20, color=config["plots"]["color_pred_test"])
plt.title("Predicted close price of the next trading day")
plt.grid(which='major', axis='y', linestyle='--')
plt.legend()
plt.show()
#%%
print("Predicted close price of the next trading day:", round(to_plot_data_y_test_pred[plot_range-1], 2))

# %%
