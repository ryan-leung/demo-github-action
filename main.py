from io import BytesIO
from typing import List

import requests
from PIL import Image
from pydantic import BaseSettings
from rss_parser import Parser


class Settings(BaseSettings):
    huggingface_api : str
    huggingface_url : str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

def get_current_trend(region_code: str) -> List[str]:
    URL=f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={region_code}"
    response = requests.get(URL)
    rss = Parser.parse(response.text)
    results = []
    for item in rss.channel.items:
        results.append(str(item.title))
    return results

def get_stable_diffusion_image(input) -> Image:
    settings = Settings()
    URL=settings.huggingface_url
    API=settings.huggingface_api
    headers = {
        'Authorization': f'Bearer {API}'
    }
    response = requests.post(URL, headers=headers, data={"input": input})
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    return image


if __name__ == "__main__":
    region_code = "US"
    data = get_current_trend(region_code)
    input = " ".join(data)
    print(input)
    image = get_stable_diffusion_image(input)
    image.save(f'data/output_{region_code}.jpg', 'JPEG')