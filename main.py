'''
Importing modules bs4, time and selenium.
'''
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from login_info import mail
from login_info import pasw
from databatase import create_db
from databatase import insert_db
'''
Using selenium module for login in fb account for crawling.
'''
# PATH for chromedriver on local driver.
# Can be different on different machines.
# Change accordingly.
PATH = r'C:/Program Files (x86)/chromedriver.exe'

# FB URL for login.
# FB URL Mobile version for crawling.
URL = 'https://www.facebook.com'
try:
    create_db()
    print('Database created!')
except Exception:
    print('Database already exist!')
    pass
'''
Selenium driver login.
'''
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get(URL)
time.sleep(2)
email = driver.find_element_by_name("email")
pswrd = driver.find_element_by_name("pass")
email.send_keys(mail)
driver.implicitly_wait(1)
pswrd.send_keys(pasw)
driver.implicitly_wait(3)
email.submit()
driver.implicitly_wait(10)

URL_M_DICT = {
    'Podnájom a prenajom v Bratislave': 'https://mbasic.facebook.com/groups/967141123346624',
    'Prenájom a podnájom - Bratislava, bez realitky': 'https://mbasic.facebook.com/groups/724349171023932/',
    'Bývanie a prenájom Bratislava': 'https://mbasic.facebook.com/groups/1583434415266071/',
    'Bratislava - Bývanie, Spolubývanie, nájom, pronájom, podnájom, byt': 'https://mbasic.facebook.com/groups/123700788304715/',
    'Prenájom Bytu Bratislava': 'https://mbasic.facebook.com/groups/673598812677373/',
    'Bývanie a prenájom BA': 'https://mbasic.facebook.com/groups/ByvanieaprenajomBA/',
    '‎Podnájom, prenájom, predaj ubytko Bratislava ┃ BratislavaDen.sk': 'https://mbasic.facebook.com/groups/prenajom.predaj.bratislava/',
    'PRENÁJOM / PODNÁJOM/ / UBYTOVANIE - BRATISLAVA': 'https://www.facebook.com/groups/118942498712191/',
    'PRENAJOM A BÝVANIE PRIAMO NA MAJITELA (BEZ REALITKU) BRATISLAVA': 'https://www.facebook.com/groups/195337991035144/',
    'Prenájom bez realitky Bratislava - Realhome.sk': 'https://www.facebook.com/groups/198979500594416/',
    'Bývanie Bratislava - Byty, Domy, Pozemky - Predaj, Kúpa, Prenájom': 'https://www.facebook.com/groups/498952127151491/',
    'PRENÁJOM a PODNÁJOM v BA': 'https://www.facebook.com/groups/PRENAJOMaPODNAJOMvBA/'
    }

class_variable = {
    1: 'cw cy di', 2: 'da dc dm', 3: 'db dd dn', 4: 'de df dg', 5: 'dc dd de'
}

list_link = []
m = 0


def posts_recursive(url_, m):
    if m < 8:
        m += 1
        driver.get(url_)
        driver.find_element_by_class_name('t').click()
        pageContent = driver.page_source
        soup = BeautifulSoup(pageContent, 'html.parser')
        for value in class_variable.values():
            try:
                posts = soup.find_all('article', class_=value)
            except Exception:
                continue

            for post in posts:
                page = (post.find('a', href=True, string='Full Story'))['href']
                list_link.append(page)

            driver.implicitly_wait(3)
        try:
            html = soup.find('a', href=True, string='See More Posts')
            page = f"https://mbasic.facebook.com/{html['href']}"

            posts_recursive(page, m)
        except Exception:
            pass


ban_words = ('hľadám', 'hladam', 'hlad')
allow_words = ('Petržalka', 'Petrzalka',
               'petrzalka', 'petržalka',
               'Petr', 'petr')


def crawling_posts(urls):
    for post in urls:
        driver.get(post)
        postContent = driver.page_source
        soup = BeautifulSoup(postContent, 'html.parser')
        text_ = soup.find_all('div', class_='bu')
        for t in text_:
            for allow in allow_words:
                if allow in t.text:
                    post_n = post.replace('mbasic', 'www')
                    print(t.text)
                    print(' ')
                    print(post_n)
                    print('--------------------------------------------')
                    insert_db(t.text, post_n)
                    print('')
                    print('Inserted into Database!')


for url_m in URL_M_DICT.values():
    posts_recursive(url_m, m)
crawling_posts(list_link)
