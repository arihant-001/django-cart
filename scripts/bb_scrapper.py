import requests
import csv
from bs4 import BeautifulSoup
headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

categories = ['fruits-vegetables', 'beverages']
columns = ['Name', 'Price', 'IMG_URL', 'DESC']

for c in categories:
    url = 'https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug=' + c
    print(url)
    res = requests.get(url)
    prods = res.json()['tab_info'][0]['product_info']['products']
    file = open('./dummy_data/' + c + '.csv', 'w+', newline='')
    data = [columns]
    for i in range(0, len(prods)):
        prod_url = 'http://www.bigbasket.com' + prods[i]['absolute_url']
        soup = BeautifulSoup(requests.get(prod_url).text, "html.parser")
        divs = soup.find_all(class_='_26MFu')
        desc = '.'.join(divs[0].text.strip().split('.')[:-3])
        details = [prods[i]['p_desc'], prods[i]['mrp'], prods[i]['p_img_url'], desc]
        data.append(details)
        print(details)

    with file:
        write = csv.writer(file)
        write.writerows(data)

