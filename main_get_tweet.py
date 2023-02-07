import scraptweets
import pandas as pd
import pandas as pd

#sebelum ini, olah data1.csv menggunakan powerbi sehingga menciptakan file baru bernama data_taman_jakarta.csv
#sebenarnya lat & long di data1.csv terletak pada link nya, jadi pisahkan itu terlebih dahulu
#namun, saya sudah ada file data_taman_jakarta.csv yang sudah diolah dari data1.csv jadi code akan tetap berjalan

df = pd.read_csv("data_taman_jakarta.csv") #read csv kumpulan dari hasil taman taman
for i in range(374):
    lat = df["lat"][i]
    long = df["long"][i]
    name = df["name"][i]
    scraptweets.scraptweet(name,lat,long)
    print(f"{name}, berhasil dengan latlong {lat},{long}")