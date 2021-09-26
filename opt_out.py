from bs4 import BeautifulSoup

import os, csv, re, time, requests
from inspect import getsourcefile
from os.path import abspath

from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
# from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
#
# from selenium.webdriver.common.by import By

import PyPDF2


file_path = abspath(getsourcefile(lambda _: None))
file_dir = os.path.normpath(file_path + os.sep + os.pardir)

chromedriver = os.path.join(file_dir, "chromedriver.exe")
os.chmod(chromedriver, int('0755'))
os.environ["webdriver.chrome.driver"] = chromedriver
op = webdriver.ChromeOptions()
p = {"download.default_directory": "C:\\Users\\aiden\\Desktop\\python\\data_privacy\\downloads",
     "safebrowsing.enabled": "false"}
op.add_experimental_option("prefs", p)
# driver = webdriver.Chrome(chrome_options=op)



def download_pdf(business_id, business_name):
  driver = webdriver.Chrome(chromedriver, chrome_options=op)

  driver.get("https://bizfilings.vermont.gov/online/BusinessInquire/FilingHistory?businessID=%s"%business_id)

  # driver.find_element_by_xpath("/html/body/article/section/form/button").click()

  # driver.FindElement(By.LinkText("DATA BROKER REGISTRATION")).Click();
  # driver.find_element(By.XPATH, 'DATA BROKER REGISTRATION')
  driver.find_element_by_xpath("//*[text()='DATA BROKER REGISTRATION']").click()

  time.sleep(8)
  driver.close()

  for root, subs, files in os.walk("downloads"):
    for file in files:
      if file.startswith('000'):
        os.rename(os.path.join(root, file), os.path.join(root, business_name+'.pdf'))
  time.sleep(1)
  return 1
'''

<a href="javascript: void(0)" onclick="SubmitThisForm('C:\\Documents\\DatabrokerReg\\000238493\\0353086\\Correspondence\\2013570056_496038.pdf','0002511191')">DATA BROKER REGISTRATION</a>
'''

def scrape_pdf():

  # open the pdf file
  object = PyPDF2.PdfFileReader("test.pdf")

  # get number of pages
  NumPages = object.getNumPages()

  # define keyterms
  String = "What was the method for requesting an opt-out"

  # extract text and do the search
  for i in range(0, NumPages):
    PageObj = object.getPage(i)
    print("this is page " + str(i))
    Text = PageObj.extractText()
    # print(Text)
    ResSearch = re.search(String, Text)
    if ResSearch:

      Text = Text.replace('€€€€VERMONT SECRETARY OF STATE Corporations Division MAILING ADDRESS: Vermont Secretary of State, 128 State Street, Montpelier, VT 05633-1104 DELIVERY ADDRESS: Vermont Secretary of State, 128 State Street, Montpelier, VT 05633-1104 PHONE: 802-828-2386 € € € € € € € € € € € € WEBSITE: www.sec.state.vt.us ', '')
      Text = Text.replace('€', '')

      print(ResSearch)
      return Text
      # from_delim = 'What was the method for requesting an opt-out?'
      # to_delim = ''

base_url = 'https://www.fastcompany.com/90310803/here-are-the-data-brokers-quietly-buying-and-selling-your-personal-information'
r = requests.get(base_url)
html_content = r.text
soup = BeautifulSoup(html_content, 'lxml')


links = soup.find_all('a')

links_to_shitbox_companies = [a for a in links if 'vtsos' in a.attrs.get('href', '')]

# print(len(links_to_shitbox_companies))

shitbox_companies = [(b.attrs.get('href', '').split('=')[1], b.text) for b in links_to_shitbox_companies]

path = '/downloads'

# Check whether the specified path exists or not
isExist = os.path.exists(path)

if not isExist:
  # Create a new directory because it does not exist
  os.makedirs(path)
  print("The new directory is created!")


with open('opt_out.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')#,quotechar='|', quoting=csv.QUOTE_MINIMAL)

  for business_id, business_name in shitbox_companies:
    #download the pdf
    # url = 'https://bizfilings.vermont.gov/online/BusinessInquire/BusinessInformation?businessID=%s'%business_id
    download_pdf(business_id, business_name)

    #get the opt-out info by reading the pdf
    # out_instructions =  scrape_pdf()

    # spamwriter.writerow([business_id, business_name, 'Wonderful Spam'])












def never_was():
  import requests

  session = requests.Session()
  session.verify = False


  url = "https://bizfilings.vermont.gov/online/BusinessInquire/FilingHistoryPost"

  payload='__RequestVerificationToken=SA7j42ROSIWfMVSDSmivy0rtD1sYumGgq_0TIdHQih-ZqsQgFgoWuG8bGuZxLESFC6pUjl0OLl_c6O656SrhEPGtEXPnuhGtrN6sX-cIyF1OlIF1LE3YNOUWWUtG-ZYuZcKrMBvJ8BhDLY5ghUmaExBfcMu3RM0Y7oWLJbYW0x01&hdnTotalPgCount=1&hdnFileName=C%3A%5CDocuments%5CDatabrokerReg%5C000238493%5C0353086%5CCorrespondence%5C2013570056_496038.pdf&hdnFilingNumber=0002511191&hdnFileNotFound='
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://bizfilings.vermont.gov',
    'Connection': 'keep-alive',
    'Referer': 'https://bizfilings.vermont.gov/online/BusinessInquire/FilingHistory?businessID=353086',
    'Cookie': 'ASP.NET_SessionId=5c3oavhlurdv2q1jckvugp0a; __RequestVerificationToken=D8ah4mPdJ1dUuRByXqdWVojHa6678CNbTwDey0pZQcvZaWXPFHPZX2btspAK9GzPq9fRFbMZPcstZTJRKmCIoT0WufwUt00b61pMfvZSGRtchHfZQ2PzTv6J1u8qGWjOQCruM-TBM6Ryj562ert1GA2; visid_incap_2276107=RaH9L0F7THqXLma0tvzG5jCeUGEAAAAAQUIPAAAAAAC9OHuPCU+uPDcU2y/XkIvJ; incap_ses_1443_2276107=QurYWHWz9FZ/EYXV75AGFDGeUGEAAAAARNjQWr57mjcRGvjj6syfJg==',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers'
  }

  response = session.post(url=url, data=payload)#requests.request("POST", url, headers=headers, data=payload)

  print(response.text)
