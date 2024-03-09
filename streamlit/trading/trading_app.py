import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# print(sns.get_dataset_names())
df = sns.load_dataset('anagrams')
# df['attnr'] = df['attnr'].astype('category')
# df['attnr_codes'] = df['attnr'].cat.codes
# c = alt.Chart(df).mark_circle().encode(
#     x='num1', y='num2', size='attnr', color='attnr'
# )


# df2 = pd.DataFrame(
#      np.random.randn(200, 3),
#      columns=['a', 'b', 'c'])
# c = alt.Chart(df2).mark_circle().encode(
#      x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
# st.write(c)

# The title of the application
st.title('Options Trading App')
# st.write(c)
st.dataframe(df)
# st.write(stdf)

# if st.button('Say hello'):
#     st.write('Why hello there')
# else:
#     st.write('Goodbye')