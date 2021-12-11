import time
import pandas as pd
import requests as r

from bs4 import BeautifulSoup as bs
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials


def scrape():
    # load html of page and parse
    page = r.get('https://www.szcb.cz')
    soup = bs(page.content, "html.parser")

    datalist = []

    # find all elements p and select 25th element of result list
    all_p = soup.find_all("p")
    o = all_p[25].find("span").contents

    # prepare data and time
    d = time.strftime("%Y-%m-%d %H:%M:%S.000000", time.localtime())

    # prepare list of values
    datalist.append(d)
    datalist.append(int(o[0]))
    datalist = [datalist]

    # convert to dataframe
    df = pd.DataFrame(datalist)

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    cred = ServiceAccountCredentials.from_json_keyfile_name("deepnote.json", scope)

    # download dataframe from GS
    ddf = g2d.download(gfile="12DQLmzuFoxu_xK253xB4u-e-CfS6bSHj0cnM2_wb_3Y", credentials=cred, row_names=True,
                       start_cell='A2')
    final_df = pd.concat([ddf, df], ignore_index=True)

    # upload updated dataframe to GS
    spreadsheet_key = '12DQLmzuFoxu_xK253xB4u-e-CfS6bSHj0cnM2_wb_3Y'
    wks_name = 'data'
    d2g.upload(final_df, spreadsheet_key, wks_name, credentials=cred, row_names=True, clean=True, col_names=True)
