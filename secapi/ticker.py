import pandas as pd
import requests
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json, re

from metrics import key_metrics, key_metric_synonyms
from metric_matching import match_columns

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)


class UserSettings:
    def __init__(self, email):
        self.email = email

class Ticker:
    def __init__(self, ticker, user_settings):
        self.ticker = ticker
        self.__user_settings = user_settings
        self.__user_agent = {"User-Agent":self.__user_settings.email}
        self.key_metrics = key_metrics
        self.key_metric_synonyms = key_metric_synonyms

    def get_email(self):
      return self.__user_settings.email

    def get_header(self):
      return self.__user_agent

    def get_ticker(self):
      return self.ticker

    def cik(self):
      json = requests.get("https://www.sec.gov/files/company_tickers.json", headers=self.__user_agent).json()
      for i in json:
        if json[i]["ticker"] == self.ticker.upper().replace('.','-'):
          return str(json[i]["cik_str"]).zfill(10)
      raise Exception("Ticker not found")
    def get_facts(self):
      company_cik = self.cik()
      url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{company_cik}.json"
      company_facts = requests.get(url, headers=self.__user_agent).json()
      us_gaap_data = company_facts['facts']['us-gaap']
      df_data = []
      for fact, details in us_gaap_data.items():
        for unit in details["units"]:
          for item in details["units"][unit]:
            row = item.copy()
            row["fact"] = fact
            df_data.append(row)
      df = pd.DataFrame(df_data)
      df["end"] = pd.to_datetime(df["end"])
      df["start"] = pd.to_datetime(df["start"])
      df = df.drop_duplicates(subset=["fact","end","val"])
      df.set_index("end", inplace=True)
      labels_dict = {fact: details["label"] for fact, details in us_gaap_data.items()}
      return df, labels_dict
    def annual_facts(self):
      df, label_dict = self.get_facts()
      ten_k = df[df["form"] == "10-K"]
      pivot = ten_k.pivot_table(values="val", columns="fact", index="accn")
      pivot.rename(columns=label_dict, inplace=True)
      pivot['year'] = pivot.index
      pivot['year'] = pivot['year'].apply(lambda x: int(x[11:13])+2000)
      pivot = pivot.sort_values(by=['year'])
      pivot['accn'] = pivot.index
      pivot = pivot.set_index('year')
      return pivot
    def quarter_facts(self):
      df, label_dict = self.get_facts()
      ten_q = df[df["form"] == "10-Q"]
      pivot = ten_q.pivot_table(values="val", columns="fact", index="end")
      pivot.rename(columns=label_dict, inplace=True)
      return pivot
    def income_statement(self,yearly=True):
      if yearly:
        mapping = match_columns(self.annual_facts())
        return self.annual_facts()[mapping['Income Statement']]
      else:
        mapping = match_columns(self.quarter_facts())
        return self.quarter_facts()[mapping['Income Statement']]
    def balance_sheet(self,yearly=True):
      if yearly:
        mapping = match_columns(self.annual_facts())
        return self.annual_facts()[mapping['Balance Sheet']]
      else:
        mapping = match_columns(self.quarter_facts())
        return self.quarter_facts()[mapping['Balance Sheet']]
    def cash_flow_statement(self,yearly=True):
      if yearly:
        mapping = match_columns(self.annual_facts())
        return self.annual_facts()[mapping['Cash Flow Statement']]
      else:
        mapping = match_columns(self.quarter_facts())
        return self.quarter_facts()[mapping['Cash Flow Statement']]


