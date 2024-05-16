from modeling import Modeling
from load_data import initialize_project
from kafka_producer import send_data_to_kafka
import streamlit as st

def main():
    st.title('Alpha Vantage Price Prediction')
    symbol = st.text_input(label="Enter symbol")
    if st.button("Predict"):
        m = Modeling(symbol)
        send_data_to_kafka("stock-data")
        m.make_model()
        xgb = m.get_model()
        xgb.fit(m.X_train, m.y_train)
        preds = xgb.predict(m.df_transposed.drop('close', axis=1).tail(1))

        st.write(f"${round(float(preds[0]), 2)}")


if __name__ == "__main__":
    main()