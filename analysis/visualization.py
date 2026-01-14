import matplotlib.pyplot as plt
import pandas as pd

def plot_rolling_signal(df: pd.DataFrame):

    df =df.copy()
    df["timestamp"]= pd.to_datetime(df["timestamp"], errors="coerce")
    df= df.dropna(subset=["timestamp"])

    df.set_index("timestamp", inplace=True)

    rolling_signal= df["final_signal"].rolling("15min").mean()

    rolling_signal.plot(title="Rolling Market Sentiment Signal (15 min)")
    plt.tight_layout()
    plt.show()
