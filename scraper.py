import time
import pandas as pd
import requests as r

from bs4 import BeautifulSoup as bs
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials


def scrape():
    page = r.get('https://www.szcb.cz')
    soup = bs(page.content, "html.parser")

    l_ist = []
    all_p = soup.find_all("p")
    o = all_p[25].find("span").contents

    d = time.strftime("%d.%m.%Y", time.localtime())
    t = time.strftime("%H:%M:%S", time.localtime())

    l_ist.append(d)
    l_ist.append(t)
    l_ist.append(int(o[0]))
    l_ist = [l_ist]

    df = pd.DataFrame(l_ist)

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    cred = ServiceAccountCredentials.from_json_keyfile_name("deepnote.json", scope)

    ddf = g2d.download(gfile="12DQLmzuFoxu_xK253xB4u-e-CfS6bSHj0cnM2_wb_3Y", credentials=cred, row_names=True, start_cell='A2')
    final_df = pd.concat([ddf, df], ignore_index=True)

    spreadsheet_key = '12DQLmzuFoxu_xK253xB4u-e-CfS6bSHj0cnM2_wb_3Y'
    wks_name = 'data'
    d2g.upload(final_df, spreadsheet_key, wks_name, credentials=cred, row_names=True, clean=True, col_names=True)
