import taipy
import plotting, predict, data_info
from taipy import Gui
import seaborn as sns

df = data_info.load_data('taipy/tpy1/tpy1/data/water.csv')
print(df.head())
df_json = df.to_json('temp.json', orient='records')
# fig = sns.countplot(df, x="Geographic_area")

Gui("<|{df}|chart|type=bar|y=REF_AREA:Geographic area|>").run()
# <|{df}|table|>
