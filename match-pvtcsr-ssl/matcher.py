import requests
from urllib.parse import quote

def data(csrpvt, cert):
    newcsrpvt = quote(csrpvt)
    newcert = quote(cert)
    input_data = f"MatcherForm%5Bssl_cert%5D={newcert}&CsrOrPrivat_cert=&MatcherForm%5Bother_cert%5D={newcsrpvt}"
    return input_data

# Define the function to make the POST request
def fetch_data(csrpvt, cert):
    input_data = data(csrpvt, cert)
    url = "https://www.sslchecker.com/matcher"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.sslchecker.com/matcher",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.post(url, headers=headers, data=input_data)
    if response.ok:
        html = response.text
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        span_element = soup.select_one('.info-block3.ok > div > span')
        if span_element:
            extracted_text = span_element.get_text(strip=True)
            return extracted_text
        else:
            return "CSR/Private Key and Certificate do not match"
    else:
        print('There was a problem with the fetch operation:', response.status_code)
