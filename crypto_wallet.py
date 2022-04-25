# Version: 1.04
# 2021-01-09 Add to git
# 2021-12-12 Add reading values from EXCEL
# 2021-11-11 Add charts, add try, except
# 2021-11-05 Changed MANA
import requests
from tkinter import messagebox as mbox
import tkinter as tk  # link: https://stackoverflow.com/questions/17466561/best-way-to-strucd yhn6ture-a-tkinter-application
import tkinter.ttk as ttk
import json
import pandas # for reading data from xlsx
import matplotlib.pyplot as plt # for charts
import numpy as np # do wykresów

# todo: dodać jakoś wskaźnik z score 
# https://www.lookintobitcoin.com/charts/mvrv-zscore/
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # CZĘŚC GÓRNA
        self.frame_Top_Glowna = tk.Frame(root)
        self.frame_Top_Glowna.pack(fill='x')
        self.lbl_Tytul = tk.Label(self.frame_Top_Glowna, text="System analiz przebiegu", bg='yellow')
        self.lbl_Tytul.grid(row=1, column=0)
        self.frame_Kursy = ttk.LabelFrame(root, text="Kursy")
        self.frame_Kursy.pack(fill='x')

        padx = 10
        pady = 1

        def tworz_lbl_kurs(self, para, wiersz):
            """Tworzenie wiersza z labelami"""
            if (para == "USD-PLN"):
                try:
                    kurs_USD = MainApplication.kurs_FIAT(self, "usd")
                except:
                    kurs_USD = 0

                self.label0 = tk.Label(self.frame_Kursy, bg='white', font=(None, 12), width=10, anchor='e')
                self.label0.grid(row=wiersz, column=0, sticky='E', padx=padx, pady=pady)
                self.label0.config(text=para)
                self.label1 = tk.Label(self.frame_Kursy, bg='white', font=(None, 12), width=10, anchor='w')
                self.label1.grid(row=wiersz, column=2, sticky='W', pady=pady)
                self.label1.config(text=kurs_USD)
                self.label2 = tk.Label(self.frame_Kursy, bg='white', font=(None, 12), width=6, anchor='e')
                self.label2.grid(row=wiersz, column=3, sticky='E', padx=padx, pady=pady)
                self.label2.config(text="zł")
            else:
                self.label0 = tk.Label(self.frame_Kursy, bg='white', font=(None, 12), width=10, anchor='e')
                self.label0.grid(row=wiersz, column=0, sticky='E', padx=padx, pady=pady)
                self.label0.config(text=para)
                self.label1 = tk.Label(self.frame_Kursy, bg='white', font=(None, 12), width=10, anchor='w')
                self.label1.grid(row=wiersz, column=2, sticky='W', pady=pady)
                self.label1.config(text=MainApplication.kurs(self, para))
                self.label2 = tk.Label(self.frame_Kursy, bg='white', font=(None, 12), width=6, anchor='e')
                self.label2.grid(row=wiersz, column=3, sticky='E', padx=padx, pady=pady)
                self.label2.config(text="zł/1 szt")

        wallet_binance = {}
        wallet_bitbay = {}
        wallet_revolut = {}
        def fill_wallet(self):
            nonlocal wallet_binance
            nonlocal wallet_bitbay
            nonlocal wallet_revolut
            path = r'2022 PORTFEL.xlsx'
            excel_data = pandas.read_excel(path, sheet_name='KRYPTOWALUTY')  # , usecols=['Waluta', 'BITBAY']
            excel_data.set_index('Waluta')
            wal = 'BTC'
            a = excel_data.where(excel_data == 'XRP').dropna(how='all').dropna(axis=1)
        tworz_lbl_kurs(self, "BTC-PLN", 2)
        tworz_lbl_kurs(self, "XRP-PLN", 3)
        tworz_lbl_kurs(self, "XLM-PLN", 4)
        tworz_lbl_kurs(self, "ETH-PLN", 5)
        tworz_lbl_kurs(self, "DOGE-PLN", 6)
        tworz_lbl_kurs(self, "USD-PLN", 7)

        self.frame_finanse = ttk.LabelFrame(root, text="Dane finansowe")
        self.frame_finanse.pack(fill='x')
        padx = 1
        pady = 1
        font = (None, 7, "bold")
        
        # Tworzenie naglowka tabeli
        self.lbl_ilosc_header = tk.Label(self.frame_finanse, text="Ilość", bg='white', width=12, font=font, name="lbl_ilosc_header")
        self.lbl_ilosc_header.grid(row=0, column=1, sticky='E', padx=padx, pady=pady)
        self.lbl_waluta_header = tk.Label(self.frame_finanse, text="Wal", bg='white', width=5, font=font, name="lbl_waluta_header")
        self.lbl_waluta_header.grid(row=0, column=2, sticky='E', padx=padx, pady=pady)
        self.lbl_kwota_konw_header = tk.Label(self.frame_finanse, text="Kwota", bg='white', width=10, font=font, name="lbl_kwota_konw_header")
        self.lbl_kwota_konw_header.grid(row=0, column=3, sticky='E', padx=padx, pady=pady)
        self.lbl_kwota_rze_header = tk.Label(self.frame_finanse, text="Bilans", bg='white', width=10, font=font, name="lbl_kwota_rze_header")
        self.lbl_kwota_rze_header.grid(row=0, column=4, sticky='E', padx=padx, pady=pady)
        self.lbl_kwota_zysk_header = tk.Label(self.frame_finanse, text="Zysk/strata.", bg='white', width=10, font=font, name="lbl_kwota_zysk_header")
        self.lbl_kwota_zysk_header.grid(row=0, column=5, sticky='E', padx=padx, pady=pady)
        # wczytanie stanu poczatkowego
        path = r'2022 PORTFEL.xlsx'
        excel_data = pandas.read_excel(path, sheet_name='KRYPTOWALUTY')  # , usecols=['Waluta', 'BITBAY']
        excel_data.set_index('Waluta')
        wal = 'BTC'
        a = excel_data.where(excel_data == 'XRP').dropna(how='all').dropna(axis=1)
        # print(excel_data.loc[a.index[0], 'BITBAY'])
        print(excel_data.loc[excel_data.where(excel_data == 'BTC').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'])
        # print(excel_data.loc['BTC', 'KRYPTOWALUTY'])
        ilosc_BTC = round(excel_data.loc[excel_data.where(excel_data == 'BTC').dropna(how='all').dropna(axis=1).index[0], 'Revolut'],8)
        ilosc_XRP = round(excel_data.loc[excel_data.where(excel_data == 'XRP').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_XLM =  round(excel_data.loc[excel_data.where(excel_data == 'XLM').dropna(how='all').dropna(axis=1).index[0], 'Revolut'],8)
        ilosc_ETH =  round(excel_data.loc[excel_data.where(excel_data == 'ETH').dropna(how='all').dropna(axis=1).index[0], 'Revolut'],8)
        ilosc_DOGE = round(excel_data.loc[excel_data.where(excel_data == 'DOGE').dropna(how='all').dropna(axis=1).index[0], 'BINANCE'],8)
        ilosc_ALG = round(excel_data.loc[excel_data.where(excel_data == 'ALG').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_AMLT = round(excel_data.loc[excel_data.where(excel_data == 'AMLT').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_BOB = round(excel_data.loc[excel_data.where(excel_data == 'BOB').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_LML = round(excel_data.loc[excel_data.where(excel_data == 'LML').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_MANA = round(excel_data.loc[excel_data.where(excel_data == 'MANA').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_XIN = round(excel_data.loc[excel_data.where(excel_data == 'XIN').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_NEU = round(excel_data.loc[excel_data.where(excel_data == 'NEU').dropna(how='all').dropna(axis=1).index[0], 'ZONDA'],8)
        ilosc_SHIB = round(excel_data.loc[excel_data.where(excel_data == 'SHIB').dropna(how='all').dropna(axis=1).index[0], 'BINANCE'],8)
        ilosc_LRC = round(excel_data.loc[excel_data.where(excel_data == 'LRC').dropna(how='all').dropna(axis=1).index[0], 'Revolut'],8)
        ilosc_YFI = round(excel_data.loc[excel_data.where(excel_data == 'YFI').dropna(how='all').dropna(axis=1).index[0], 'Revolut'],8)
        ilosc_OXT = round(excel_data.loc[excel_data.where(excel_data == 'OXT').dropna(how='all').dropna(axis=1).index[0], 'Revolut'],8)
        ilosc_FTM = round(excel_data.loc[excel_data.where(excel_data == 'FTM').dropna(how='all').dropna(axis=1).index[0], 'BINANCE'],8)
        ilosc_USDT = round(excel_data.loc[excel_data.where(excel_data == 'USDT').dropna(how='all').dropna(axis=1).index[0], 'BINANCE'],8)
        ilosc_EUR = round(excel_data.loc[excel_data.where(excel_data == 'EUR').dropna(how='all').dropna(axis=1).index[0], 'Revolut'],8)

        ilosc_inw_BTC = round(excel_data.loc[excel_data.where(excel_data == 'BTC').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_XRP = round(excel_data.loc[excel_data.where(excel_data == 'XRP').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_XLM = round(excel_data.loc[excel_data.where(excel_data == 'XLM').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_ETH = round(excel_data.loc[excel_data.where(excel_data == 'ETH').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_DOGE = round(excel_data.loc[excel_data.where(excel_data == 'DOGE').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)

        ilosc_inw_ALG =  round(excel_data.loc[excel_data.where(excel_data == 'ALG').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_AMLT = round(excel_data.loc[excel_data.where(excel_data == 'AMLT').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_BOB = round(excel_data.loc[excel_data.where(excel_data == 'BOB').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_LML = round(excel_data.loc[excel_data.where(excel_data == 'LML').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_MANA = round(excel_data.loc[excel_data.where(excel_data == 'MANA').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_XIN = round(excel_data.loc[excel_data.where(excel_data == 'XIN').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_NEU = round(excel_data.loc[excel_data.where(excel_data == 'NEU').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_SHIB = round(excel_data.loc[excel_data.where(excel_data == 'SHIB').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_LRC = round(excel_data.loc[excel_data.where(excel_data == 'LRC').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_YFI = round(excel_data.loc[excel_data.where(excel_data == 'YFI').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_OXT = round(excel_data.loc[excel_data.where(excel_data == 'OXT').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_FTM = round(excel_data.loc[excel_data.where(excel_data == 'FTM').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_USDT = round(excel_data.loc[excel_data.where(excel_data == 'USDT').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        ilosc_inw_EUR = round(excel_data.loc[excel_data.where(excel_data == 'EUR').dropna(how='all').dropna(axis=1).index[0], 'RAZEM'],8)
        suma = 0
        suma_zysk = 0
        def draw_chart(self):
            currency = (str(self.widget).split(".")[-1])[8:]
            names = ['group_a', 'group_b', 'group_c']
            values = [1, 10, 100]
            plt.figure(figsize=(10.3, 7))
            plt.plot([1, 2, 3, 4])
            plt.ylabel('some numbers')
            plt.show()
        def tworz_lbl_finanse(self, waluta, wiersz):
            """Procedura do tworzenia lbl w cz. finansowej"""
            nonlocal suma
            nonlocal suma_zysk
            ilosc_waluty = 0
            ilosc_akt_pln = 0
            if waluta == "BTC":
                ilosc_waluty = ilosc_BTC
                ilosc_akt_pln = ilosc_inw_BTC
            elif waluta == "XRP":
                ilosc_waluty = ilosc_XRP
                ilosc_akt_pln = ilosc_inw_XRP
            elif waluta == "XLM":
                ilosc_waluty = ilosc_XLM
                ilosc_akt_pln = ilosc_inw_XLM
            elif waluta == "ETH":
                ilosc_waluty = ilosc_ETH
                ilosc_akt_pln = ilosc_inw_ETH
            elif waluta == "DOGE":
                ilosc_waluty = ilosc_DOGE
                ilosc_akt_pln = ilosc_inw_DOGE
            elif waluta == "ALG":
                ilosc_waluty = ilosc_ALG
                ilosc_akt_pln = ilosc_inw_ALG
            elif waluta == "AMLT":
                ilosc_waluty = ilosc_AMLT
                ilosc_akt_pln = ilosc_inw_AMLT
            elif waluta == "BOB":
                ilosc_waluty = ilosc_BOB
                ilosc_akt_pln = ilosc_inw_BOB
            elif waluta == "LML":
                ilosc_waluty = ilosc_LML
                ilosc_akt_pln = ilosc_inw_LML
            elif waluta == "MANA":
                ilosc_waluty = ilosc_MANA
                ilosc_akt_pln = ilosc_inw_MANA
            elif waluta == "XIN":
                ilosc_waluty = ilosc_XIN
                ilosc_akt_pln = ilosc_inw_XIN
            elif waluta == "NEU":
                ilosc_waluty = ilosc_NEU
                ilosc_akt_pln = ilosc_inw_NEU
            elif waluta == "SHIB":
            	ilosc_waluty = ilosc_SHIB
            	ilosc_akt_pln = ilosc_inw_SHIB
            elif waluta == "LRC":
            	ilosc_waluty = ilosc_LRC
            	ilosc_akt_pln = ilosc_inw_LRC
            elif waluta == "YFI":
            	ilosc_waluty = ilosc_YFI
            	ilosc_akt_pln = ilosc_inw_YFI
            elif waluta == "OXT":
            	ilosc_waluty = ilosc_OXT
            	ilosc_akt_pln = ilosc_inw_OXT
            elif waluta == "FTM":
            	ilosc_waluty = ilosc_FTM
            	ilosc_akt_pln = ilosc_inw_FTM
            elif waluta == "USDT":
            	ilosc_waluty = ilosc_USDT
            	ilosc_akt_pln = ilosc_inw_USDT
            elif waluta == "EUR":
            	ilosc_waluty = ilosc_EUR
            	ilosc_akt_pln = ilosc_inw_EUR
            font=(None, 7)
            lista_walut_binance = ['SHIB', 'LRC', 'YFI', 'OXT', 'FTM']
            lista_walut_fiat = ['EUR']
            if waluta in lista_walut_binance:
                try:
                	kurs_USD = MainApplication.kurs_FIAT(self, "usd")
                except:
                	kurs_USD = 4
                kwota_konw = "{:.2f}".format(
                    ilosc_waluty * float(MainApplication.kurs_binance(self, waluta + "USDT"))*kurs_USD)
            elif  waluta in lista_walut_fiat:
                try:
                    kurs_EUR = MainApplication.kurs_FIAT(self, "eur")
                except:
                    kurs_EUR = 4.6

                kwota_konw = "{:.2f}".format(
                    ilosc_waluty * kurs_EUR)
            else:
                kwota_konw = "{:.2f}".format(ilosc_waluty * float(MainApplication.kurs(self, waluta + "-PLN")))

            zysk_strata = "{:.2f}".format( float(kwota_konw) + float(ilosc_akt_pln) )
            suma_zysk = suma_zysk + float(zysk_strata)
            self.lbl_ilosc = tk.Label(self.frame_finanse, text=ilosc_waluty, bg='white', width=12, name="lbl_ilosc"+str(wiersz), font=font)
            self.lbl_ilosc.grid(row=wiersz, column=1, sticky='W', padx=padx, pady=pady)
            self.lbl_waluta = tk.Label(self.frame_finanse, text=waluta, bg='white', width=5, name="lbl_waluta"+str(wiersz), font=font)
            self.lbl_waluta.grid(row=wiersz, column=2, sticky='E', padx=padx, pady=pady)
            self.lbl_kwota_konw = tk.Label(self.frame_finanse, text=kwota_konw, bg='white', width=10, name="lbl_kwota_konw"+str(wiersz), font=font)
            suma = suma + float(kwota_konw)
            self.lbl_kwota_konw.grid(row=wiersz, column=3, sticky='E', padx=padx, pady=pady)
            self.lbl_kwota_rze = tk.Label(self.frame_finanse, text=ilosc_akt_pln, bg='white', width=10, name="lbl_ilosc_akt_pln"+str(wiersz), font=font)
            self.lbl_kwota_rze.grid(row=wiersz, column=4, sticky='E', padx=padx, pady=pady)
            if (float(zysk_strata)<0):
                kolor='red'
            else:
                kolor='green'
            self.lbl_zysk = tk.Label(self.frame_finanse, text=zysk_strata, bg=kolor, width=10, name="lbl_zysk"+waluta, font=font)
            self.lbl_zysk.grid(row=wiersz, column=5, sticky='W', padx=padx, pady=pady)
            self.lbl_zysk.bind("<Button-1>", draw_chart)
        tworz_lbl_finanse(self, "BTC", 1)
        tworz_lbl_finanse(self, "XRP", 2)
        tworz_lbl_finanse(self, "XLM", 3)
        tworz_lbl_finanse(self, "ETH", 4)
        tworz_lbl_finanse(self, "DOGE", 5)
        tworz_lbl_finanse(self, "ALG", 6)
        tworz_lbl_finanse(self, "AMLT", 7)
        tworz_lbl_finanse(self, "BOB", 8)
        tworz_lbl_finanse(self, "LML", 9)
        tworz_lbl_finanse(self, "MANA", 10)
        tworz_lbl_finanse(self, "XIN", 11)
        tworz_lbl_finanse(self, "NEU", 12)
        tworz_lbl_finanse(self, "SHIB", 13)
        tworz_lbl_finanse(self, "LRC", 14)
        tworz_lbl_finanse(self, "YFI", 15)
        tworz_lbl_finanse(self, "OXT", 16)
        tworz_lbl_finanse(self, "FTM", 17)
        # tworz_lbl_finanse(self, "EUR", 18)
        lbl_podsuma = tk.Label(root, font=(None, 12), text='Aktywa: ' + str(round(suma,2)))
        lbl_podsuma.pack(side="left")
        lbl_podsuma_zysk = tk.Label(root, font=(None, 12), text=', Zysk: ' + str(round(suma_zysk, 2)))
        lbl_podsuma_zysk.pack(side="left")

        def wypisz_wszystkie_widgety(self, frame):
            for widg in frame.winfo_children():
                print(str(widg).split(".")[-1])

        # wypisz_wszystkie_widgety(self, self.frame_finanse)
        
        self.frame_dol = ttk.Frame(root)
        self.frame_dol.pack(side="bottom")
        btn_Zamknij = tk.Button(self.frame_dol, text='Zamknij aplikację')
        btn_Zamknij.pack(pady=10)
        # <create the rest of your GUI here>
        
        btn_Zamknij.bind("<Button-1>", MainApplication.zamknij)


    def zamknij(self):
        print('Program jest zamykany')
        root.destroy()


    def kurs(self, para):
        url = "https://api.zonda.exchange/rest/trading/ticker/" + para
        headers = {'content-type': 'application/json'}
        response = requests.request("GET", url, headers=headers)
        return json.loads(response.text)["ticker"]["rate"]


    def kurs_binance(self, para): # conversion to USD
        url = "https://api.binance.com/api/v3/ticker/price?symbol=" + para
        headers = {'content-type': 'application/json'}
        response = requests.request("GET", url, headers=headers)
        return json.loads(response.text)["price"]


    def kurs_FIAT(self, waluta):
        url = "http://api.nbp.pl/api/exchangerates/rates/a/" + waluta + "/" + "?format=json"
        headers = {'content-type': 'application/json'}
        response = requests.request("GET", url, headers=headers)
        return json.loads(response.text)["rates"][0]["mid"]




if __name__ == '__main__':
    root = tk.Tk()
    root.title('System analiz przebiegu 1.0')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
