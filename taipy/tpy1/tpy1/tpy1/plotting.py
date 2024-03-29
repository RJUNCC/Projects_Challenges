import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def dist_box(data, x):
    sns.boxplot(data, x=x)
    plt.show()
