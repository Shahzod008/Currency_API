from bs4 import BeautifulSoup
from fastapi import FastAPI
import uvicorn
import aiohttp

app = FastAPI()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = "https://www.cbr.ru/currency_base/daily/"


async def get_currency_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADERS) as response:
            soup = BeautifulSoup(await response.text(), features='html.parser')
            table = soup.find(name='table', class_='data')
            currency_data = []
            rows = table.find_all('tr')
            for row in rows[1:]:
                columns = row.find_all('td')
                currency_code = columns[1].text.strip()
                currency_unit = columns[2].text.strip()
                currency_name = columns[3].text.strip()
                exchange_rate = columns[4].text.strip()
                currency_data.append({
                    'Букв. код': currency_code,
                    'Единиц': currency_unit,
                    'Валюта': currency_name,
                    'Курс': exchange_rate
                })

            return currency_data


@app.get("/")
async def get_currency():
    currency_data = await get_currency_data()
    return currency_data


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
