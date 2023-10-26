from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def date(station, date):
    filename = "data_small/TG_STAID" + station.zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    date_ = df.loc[df['    DATE'] == date]['    DATE'].squeeze()
    return {"station": station,
            "date": date_,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def station(station):
    df = get_station_data(station)
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    df = get_station_data(station)
    result = df[df["date"].dt.year == int(year)].to_dict(orient="records")
    return result


def get_station_data(station):
    filename = "data_small/TG_STAID" + station.zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df = df.loc[df['   TG'] != -9999]
    df['   TG'] = df['   TG'] / 10
    df = df[['    DATE', '   TG']]
    df.columns = ['date', 'temperature']
    return df


if __name__ == "__main__":
    app.run(debug=True)
