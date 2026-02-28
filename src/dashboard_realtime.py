import os
import time
import pandas as pd
import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB   = os.getenv("PG_DB", "crypto_db")
PG_USER = os.getenv("PG_USER", "crypto_user")
PG_PASS = os.getenv("PG_PASS", "crypto_pass")


@st.cache_resource
def get_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        dbname=PG_DB, user=PG_USER, password=PG_PASS
    )


def load_symbols(conn):
    q = "SELECT DISTINCT symbol FROM crypto_realtime_prices ORDER BY symbol;"
    return pd.read_sql_query(q, conn)


def load_latest_data(conn, symbol: str, limit: int = 200):
    q = """
    SELECT *
    FROM crypto_realtime_prices
    WHERE symbol = %s
    ORDER BY ts DESC
    LIMIT %s;
    """
    df = pd.read_sql_query(q, conn, params=(symbol, limit))
    # biar urut waktu naik (kiri -> kanan)
    return df.sort_values("ts")


def main():
    st.set_page_config(page_title="Crypto Realtime Monitor", layout="wide")

    st.title("📈 Crypto Realtime Streaming Dashboard")

    conn = get_conn()

    # Sidebar: pilih symbol
    symbols_df = load_symbols(conn)
    if symbols_df.empty:
        st.warning("Belum ada data di database. Jalankan producer & consumer dulu.")
        return

    symbols = symbols_df["symbol"].tolist()
    symbol = st.sidebar.selectbox("Pilih Symbol", symbols, index=0)

    n_rows = st.sidebar.slider("Jumlah baris terakhir", 50, 1000, 200, step=50)
    refresh = st.sidebar.slider("Refresh (detik)", 2, 20, 5, step=1)

    placeholder = st.empty()

    while True:
        with placeholder.container():
            df = load_latest_data(conn, symbol, limit=n_rows)

            st.subheader(f"📊 Latest {n_rows} rows for {symbol}")
            st.dataframe(df)

            st.subheader("📉 Price over time")
            st.line_chart(df.set_index("ts")["price"])

        time.sleep(refresh)


if __name__ == "__main__":
    main()
