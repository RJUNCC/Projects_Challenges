import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

image = Image.open('../images/DNA.jpg')

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

""")

st.header("Enter DNA sequence")

st.header("Enter DNA Sequence")

sequence_input = ">DNA Query\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACT"