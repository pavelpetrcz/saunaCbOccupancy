import requests as r
import gspread
import pandas as pd
import time

from bs4 import BeautifulSoup as bs
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

def scrape():
    page = r.get('https://www.szcb.cz')
    soup = bs(page.content, "html.parser")

    l = []
    all_p = soup.find_all("p")
    o = all_p[25].find("span").contents

    d = time.strftime("%d.%m.%Y", time.localtime())
    t = time.strftime("%H:%M:%S", time.localtime())

    l.append(d)
    l.append(t)
    l.append(int(o[0]))
    l = [l]

    df = pd.DataFrame(l)

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    cred = ServiceAccountCredentials.from_json_keyfile_name("deepnote.json", scope)
    gc = gspread.authorize(cred)
    spreadsheet_key = '12DQLmzuFoxu_xK253xB4u-e-CfS6bSHj0cnM2_wb_3Y'
    wks_name = 'data'
    d2g.upload(df, spreadsheet_key, wks_name, credentials=cred, row_names=True)
    d2g.gspread.