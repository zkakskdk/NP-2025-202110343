import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

data = {
    "1분기": [500, 690, 1100, 1500, 1990, 1020],
    "2분기": [450, 700, 1030, 1650, 2020, 1600],
    "3분기": [520, 820, 1200, 1700, 2300, 2200],
    "4분기": [610, 900, 1380, 1850, 2420, 2550]
}

index = [2015, 2016, 2017, 2018, 2019, 2020]

df = pd.DataFrame(data, index=index)

df = df.T
df.index = ["first", "second", "third", "fourth"]

df.plot()

plt.title("2015~2020 Quarterly sales")
plt.xlabel("Quarters")
plt.ylabel("sales")

plt.xticks(range(len(df.index)), df.index)

plt.show()