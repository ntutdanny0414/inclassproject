from bs4 import BeautifulSoup
from selenium import webdriver
import re
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(options=option) 

class kkday:
    def __init__(self):
        self.alldata = dict()
        
        self.singleNewsSoup = None
        self.singleNews = dict()

    def newsurl(self):
        driver.get("https://www.kkday.com/zh-tw/product/" + self.keyWord)
        self.singleNewsSoup = BeautifulSoup(driver.page_source, 'lxml')

    def Getproductid(self):
        s = self.singleNewsSoup.find('div', class_='text-right text-light text-xs').text
        prod_id = re.search(r'[0-9]+', s)
        if prod_id in self.alldata:
            raise ValueError('Product ID is already exists.')
        
        if self.keyWord != prod_id:
            self.keyWord = prod_id.group(0)

    def GetTitle(self):
        self.singleNews['product_name'] = self.singleNewsSoup.find('div', class_='product-name').text
    
    def GetAbstract(self):
        self.singleNews['product_abstract'] = self.singleNewsSoup.find('div', class_='product-abstract').text


    def Getset_option(self):
        result = {}

        s = self.singleNewsSoup.find('ul', class_='option-group')
        allitems = s.find_all('li', class_='option-item')
        
        for item in allitems:
            package_info = {}

            # package oid
            package_oid = item['data-pkg-oid']
            
            # package title
            package_info['title'] = item.find('h4', class_='option-title').text
            package_info['currency'] = item.find('span', class_=None).text
            package_info['price'] = int(item.find('div', class_='product-pricing').find('h4').text.replace(',', ''))
            result[package_oid] = package_info
        
        self.singleNews['option_group'] = result

    def GetContent(self):
        article = self.singleNewsSoup.find('div', class_='info-content').text

        #print(article)
        
        def __process(text):
            product_info = {}
            
            t = re.search(r'電信公司：(.)+(?=\n)', text)
            if t:
                product_info['telecomm'] = t.group(0).replace('電信公司：', '')

            t = re.search(r'上網速度：(.)+(?=\n)', text)
            if t:
                product_info['speed'] = t.group(0).replace('上網速度：', '')

            t = re.search(r'流量限制：(.)+(?=\n)', text)
            if t :
                product_info['data'] = t.group(0).replace('流量限制：', '')

            t = re.search(r'熱點分享：(.)+(?=\n)', text)
            if t:
                t = t.group(0).replace('熱點分享：', '')
                product_info['is_hotspot'] = False if re.search(r'(不)', t) else True

            t = re.search(r'訊號涵蓋範圍：(.)+(?=\n)', text)
            if t :
                product_info['coverage'] = t.group(0).replace('訊號涵蓋範圍：', '')

            t = re.search(r'卡片規格：(.)+(?=\n)', text)
            if t :
                product_info['size'] = t.group(0).replace('卡片規格：', '')

            t = re.search(r'通話功能：(.)+(?=\n)', text)
            if t :
                product_info['phone_call'] = t.group(0).replace('通話功能：', '')
                t = t.group(0).replace('通話功能：', '')
                product_info['is_phone_call'] = False if re.search(r'(無)', t) else True

            return product_info

        self.singleNews['product_info'] = __process(article)


    def Getway(self):
        if len(self.singleNewsSoup.select('#voucher-type')) != 0:
            way = self.singleNewsSoup.select('#voucher-type')[0].text
            self.singleNews['voucher_type'] = way
    def Getnotice(self):
        if len(self.singleNewsSoup.select('#reminder')) != 0:
            notice = self.singleNewsSoup.select('#reminder')[0].text
            self.singleNews['reminder'] = notice
    def Getcancel(self):
        if len(self.singleNewsSoup.select('#cancellation-policy')) != 0:
            x = self.singleNewsSoup.select('#cancellation-policy')[0].text.replace('\t','').replace('\n','')
            self.singleNews['cancelation_policy'] = x
    def CrawlAllNews(self, prod_id):
        try:
            self.keyWord = prod_id
            self.newsurl()
            self.Getproductid()
            self.GetTitle()
            self.GetAbstract()
            self.Getset_option()
            self.GetContent()
            self.Getway()
            self.Getnotice()
            self.Getcancel()
            self.alldata[self.keyWord] = self.singleNews
        except:
            print('Not found')
        

#datalist = ['9809', '9810', '9835', '9836', '9837', '9908', '9972', '10267', '10692', '10954', '10978', '11096', '11175', '11702', '12417', '18451', '19283', '19417', '19462', '19497', '19944', '20127', '20552']
datalist = ['3524', '5458', '18246', '5925', '6051', '6056', '6101', '6125',
            '7366', '7367', '7368', '7423', '7452', '7587', '7595', '7596',
            '8211', '8217', '8305', '8754', '9093', '9366', '9496', '9588',
            '9667', '9675', '9811', '9814', '9817', '9828', '9838', '9867',
            '9965', '9966', '9967', '9968', '9969', '9995', '9997', '10007',
            '10010', '10012', '10020', '10021', '10026', '10031', '10224',
            '10227', '10293', '10332', '10468', '10487', '10691', '10767',
            '11157', '11185', '11347', '11375', '11378', '11379', '11653',
            '11660', '11832', '11847', '11955', '12008', '12022', '12096',
            '12143', '12218', '12364', '12801', '13339', '17689', '17754',
            '17756', '17836', '18021', '18047', '18049', '18127', '18131',
            '18137', '18149', '18168', '18218', '18240', '18246', '18346',
            '18460', '18523', '18528', '18530', '18531', '18615', '18711',
            '19072', '19072', '19291', '19307', '19390', '19553', '19639',
            '19648', '19650', '19672', '19689', '19690', '19804', '19807',
            '19834', '19906', '19908', '19991', '20101', '20537', '20581', '20721']

parser = kkday()

for i in datalist:
    print(i)
    parser.CrawlAllNews(i)
    print(parser.alldata)


import json


with open('data_final.json', 'w', encoding='utf8') as json_file:  
    json.dump(parser.alldata, json_file, indent=4, sort_keys=True, ensure_ascii=False)
