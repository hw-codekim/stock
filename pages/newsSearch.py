from bs4 import BeautifulSoup
import requests
import json

class corpList:

    def __init__(self):

        self.corp_list={
            'code':[],
            'name':[]
        }

    def make_corp_list(self):
        url = 'http://comp.fnguide.com/XML/Market/CompanyList.txt'
        res = requests.get(url)
        if res.status_code == 200:
            res.encoding = 'utf-8-sig'
            content = res.text
            dicts = json.loads(content)
            dict_corp = dicts['Co']
            for corp in dict_corp:
                self.corp_list['name'].append(corp['nm'])
                self.corp_list['code'].append(corp['cd'])
        return 

if __name__ == '__main__':
    cl = corpList()
    mcl = cl.make_corp_list()
    corplist = cl.corp_list
    name = '삼성전자'
    if corplist['name'] == name:
        corplist['name']