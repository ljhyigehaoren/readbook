import requests
import pymysql
from lxml import etree
import time,json

class qd_spider(object):

    def __init__(self):
        """

        host=None, user=None, password="",
        database=None, port=0, charset=''
        """
        self.client = pymysql.Connect(
            'localhost','root','12345678',
            'readbook',3306,charset='utf8',
        )
        self.cursor = self.client.cursor()

    def get_category_data(self):
        base_url = 'https://www.qidian.com/'
        html = self.send_request(base_url)
        etree_html = etree.HTML(html)
        dds = etree_html.xpath('//div[@id="classify-list"]//dd')
        print(len(dds))
        for dd in dds:
            item = {}
            item['name'] = dd.xpath('.//span[@class="info"]/i/text()')[0]
            item['info'] = item['name']
            item['coverImage'] = 'https://bookcover.yuewen.com/qdbimg/349573/1015105126/180'
            # print(item['title'])
            self.save_data_to_db('user_category',item)


    def get_book_data(self,category_id,page,my_category_id):
        url = 'https://www.qidian.com/all?chanId=%s&orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=%s' % (category_id,page)
        html = self.send_request(url)
        html_etree = etree.HTML(html)
        books = html_etree.xpath('//ul[@class="all-img-list cf"]/li')

        if len(books) > 0:
            for book in books:
                item = {}
                # bookid
                item['id'] = int(book.xpath('.//div[@class="book-mid-info"]/h4/a/@data-bid')[0])
                item['title'] = book.xpath('.//div[@class="book-mid-info"]/h4/a/text()')[0].replace('\r', '').replace(
                    ' ', '')
                item['info'] = book.xpath('.//p[@class="intro"]/text()')[0].replace('\r', '').replace(' ', '')
                item['author'] = book.xpath('.//p[@class="author"]/a[@class="name"]/text()')[0]
                item['stauts'] = book.xpath('.//p[@class="author"]/span/text()')[0]
                item['coverImage'] = 'https:' + book.xpath('.//div[@class="book-img-box"]/a/img/@src')[0]
                item['readNum'] = 0
                item['category_id'] = my_category_id
                item['addTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                self.save_data_to_db('user_book', item)

                self.get_chpater_info(item['id'])
            #下一页
            page += 1
            # self.get_book_data(category_id,page,my_category_id)

    def get_chpater_info(self,bookid):

        url = 'https://book.qidian.com/ajax/book/category?_csrfToken=8OyhWnktqFrH28U3A3vPhrQJ3kS9ZosqwuZCIIPd&bookId=%s' % str(bookid)
        html = self.send_request(url)
        chpater_lists = json.loads(html)['data']['vs']

        for chpater_info in chpater_lists[:2]:
            if int(chpater_info['vS']) == 0:
                # print('免费章节')
                #https://read.qidian.com/chapter/ORlSeSgZ6E_MQzCecGvf7A2/CkfURYYQdxNp4rPq4Fd4KQ2
                if len(chpater_info['cs']) > 2:
                    chpater_info['cs'] = chpater_info['cs'][0:1]
                for chpater in chpater_info['cs']:
                    chpater_url = 'https://read.qidian.com/chapter/' + chpater['cU']
                    print(chpater_url)
                    chpater_data = {}
                    chpater_data['id'] = int(chpater['id'])
                    chpater_data['title'] = chpater['cN']
                    chpater_data['size'] = int(chpater['cnt'])
                    chpater_data['type'] = 1
                    chpater_data['readNum'] = 0
                    chpater_data['addTime'] = chpater['uT']
                    chpater_data['book_id'] = bookid
                    chpater_data['content'] = self.get_chpater_content(chpater_url).lstrip('\r\n')

                    if len(chpater_data['content']) > 100:
                        # 说明有内容，则存保存至数据库
                        print(chpater_data)
                        chpater_data['content'] += ' '*1000
                        self.save_data_to_db('user_chpater',chpater_data)

    def get_chpater_content(self,chpater_url):

        html = self.send_request(chpater_url)
        if html:
            html_etree = etree.HTML(html)
            content = ''.join(html_etree.xpath('//div[@class="read-content j_readContent"]//p/text()'))
            return content.replace('\u3000\u3000','\r\n')

    def send_request(self,url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        response = requests.get(url=url,headers=header)
        if response.status_code == 200:
            #print(response.content.decode('UTF-8'))
            return response.content.decode('UTF-8')

    def save_data_to_db(self,tablename,item):
        sql = """
            INSERT INTO %s (%s) VALUES (%s)
        """ % (
            tablename,
            ','.join(item.keys()),
            ','.join(['%s']*len(item)),
        )
        # print(sql,list(item.values()))

        try:
            self.cursor.execute(sql,list(item.values()))
            self.client.commit()
        except Exception as err:
            print(err)
            self.client.rollback()


if __name__ == '__main__':

    spider = qd_spider()
    # spider.get_category_data()
    data = [(2,1,3),(22,1,4),(4,1,5),
            (15,1,6),(6,1,7),(5,1,8),
            (7,1,9),(8,1,10),(9,1,11),
            (10,1,12),(12,1,14)]
    for sub_data in data:
        spider.get_book_data(sub_data[0],1,sub_data[2])


