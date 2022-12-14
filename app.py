#### liblary untuk memanggil model pickle ####
import joblib,os
### END ###

#### Liblary untuk membuat documentasi REST API ###
from fastapi import FastAPI
#### END ###

#### Liblary untuk menjalankan server local ####
import uvicorn
### END ###

from fastapi.middleware.cors import CORSMiddleware

#### Devinisi Fast API ###
app=FastAPI()
#### END ####

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### Memanggil Model Pickle Yang Gunanya untuk insialisasi posisi model yang mau di ekseskusi dengan menggukan liblary joblib ####
phish_model = open('model/phishing.pkl','rb')
phish_model_ls = joblib.load(phish_model)
#### END ####

#### Halaman Root Awal ####
# app.get('/') adalah routelist yang nantinya di akses pertama kali misal localhost:8000/ #
# def read_root adalah suatu method #
# retrun {"heloo":"world"} fungsi yang nanti di balikan ke view #
@app.get("/")
def read_root():
    return {"Hello":"world"}
#### END ####

### Halaman untuk predict ###
# @app.get('/predict/{feature}') adalah routes list yang nantinya di akses yang membawa pramater query feature ###
# async def predict(feauteres): membuat method yang membawa paramater features unutuk menampung hasil parameter yang di tentukan #
# X_predict = [] suatu variable untuk menampung array kosong yang nantinya akan diisi value dari request data #
# X_predict.append(str(feauteres)) suatu variable yang nantinya akan di masukan ke X_predict = [] untuk di tampung ke dalam array #
# y_Predict = phish_model_ls.predict(X_predict) memanggil model yang sudah di definisakn di atas untuk predict hasil dari X_predict yang ada di dalam array #
@app.get('/predict/{feature}')
async def predict(feauteres):
    X_predict = []
    X_predict.append(str(feauteres))
    y_Predict = phish_model_ls.predict(X_predict)
    ### Logic Predict Dari hasil X_predict ###
    # jika hasil array dari X_predict yang nantinya di proses dengan y_Predict hasilnya bad nantinya akan mengembalikan string situs ini adalah pihising dan jiak hasinya bukan bad akan menghasilkan string situs ini bukan phising #
    if y_Predict == 'bad':
        result = "Situs ini tidak aman"
    else:
        result = "Kami tidak menemukan tautan ini berbahaya"
    ### END ###

    ### membuat variable data yang berisi object yang nantinya akan mengebalikan response dari request yang dikirim dan hasil yang sudah di proses dari X_predict dan y_predict dalam bentuk object ###
    data = {'url':feauteres,'data':result}
    return data

#### END ###


### salah satu fungsi untuk menjalankan local server yang menggunakan liblary uvicorn ###
if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000)
### END ###


#### Untuk Mejanlankan ####
# Masuk ke dalam terminal lalu ketik venv\Scripts\activate.bat #
# ketika sudah masuk ke dalam model venv bisa ketik di dalam terminal dengan perintah uvicorn main:app #
# ketika sudah buka browser dan menuju ke url http://127.0.0.1:8000/docs/

### END ###