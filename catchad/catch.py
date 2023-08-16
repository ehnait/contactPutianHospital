# -*-coding:utf8-*-

import requests
import re
import traceback
import random
import time
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed


# 加载关键词列表
def load_keywords():
    key_words = []
    with open('kw_city', 'r') as f_city, open('kw_hospital.txt', 'r') as f_hospital:
        city_list = [city.strip() for city in f_city.readlines()]
        hospital_list = [hospital.strip() for hospital in f_hospital.readlines()]

    if city_list and hospital_list:
        key_words = [f"{city}{hospital}" for city in city_list for hospital in hospital_list]

    return key_words


# 解析并抓取百度搜索结果
def scrape_baidu_results(keyword):
    max_page = 1

    headers = {
        "User-Agent": UserAgent().random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.baidu.com",
        # 需要更换Cookie
        "Cookie": "BIDUPSID=203BB116BAD7A21452D9A8AFCF9C36F2; PSTM=1665389661; BD_UPN=123253; BDUSS=lpQTF1OFlKZmpJZEZmQ3pHdkpqMnhzRElNUk1kU35VWFFuaEpsUVpaZWtpR3hqRVFBQUFBJCQAAAAAAAAAAAEAAABNtRgKc29sb19tc2sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKT7RGOk-0Rjfm; BDUSS_BFESS=lpQTF1OFlKZmpJZEZmQ3pHdkpqMnhzRElNUk1kU35VWFFuaEpsUVpaZWtpR3hqRVFBQUFBJCQAAAAAAAAAAAEAAABNtRgKc29sb19tc2sAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKT7RGOk-0Rjfm; BAIDUID=1088EDF2D03D0FA6EC2D052921641828:FG=1; MCITY=-:; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=002la48g8l0k258g8185087v1hnjr451f; ZFY=R:BX3g8nr3kFWuFJs0zZHFQAmnd8jgw:BJUmyeTbQuQHU:C; BAIDUID_BFESS=1088EDF2D03D0FA6EC2D052921641828:FG=1; BD_HOME=1; sugstore=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; PSINO=2; delPer=0; baikeVisitId=f3893191-471e-4462-a8dc-d1569ec1182d; H_PS_PSSID=36548_37557_37513_37684_37768_37778_37797_37539_37714_37741_26350_37789; H_PS_645EC=f126ZpPGPo4WkGeVRredI8zb2MdUoY1SWbcuKHKZLJ9PNN0gGSrKV4sXAlv3yU9gf7Sa; BDSVRTM=199; WWW_ST=1668936275987"
    }

    proxies = {
        # 如果需要请替换你自己代理
        'http': '117.0.144.14:4007',
    }

    url_template = 'http://www.baidu.com/s?wd={}&pn={}'

    results = []

    urls_to_fetch = []

    for page in range(max_page):
        url = url_template.format(keyword, page * 10)
        urls_to_fetch.append(url)

    try:
        for url in urls_to_fetch:
            response = requests.get(url, headers=headers, proxies=proxies)
            # 提取匹配项并添加到结果列表中
            pattern = r'https?://ada\.baidu\.com/site/[\w.-]+/xyl\?imid=[\w-]+'
            matches = re.findall(pattern, response.text)
            if matches:
                print(f"成功提取{len(matches)}条url: {'  '.join(matches)}")
            results.extend(matches)

    except requests.HTTPError as e:
        print('HTTPError: 请求失败，返回原因 - ' + e.reason)
    except Exception:
        traceback.print_exc()
    finally:
        return results


if __name__ == "__main__":
    keywords = load_keywords()
    # 并行处理任务
    with ThreadPoolExecutor() as executor:
        futures = []
        for keyword in keywords:
            delay = random.uniform(1, 3)
            print(f"当前关键字: {keyword} \t {delay}秒后开始提取")
            time.sleep(delay)
            future = executor.submit(scrape_baidu_results, keyword)
            futures.append(future)

        all_results = []
        for future in as_completed(futures):
            result = future.result()
            all_results.extend(result)

    with open('../api.txt', 'r+') as file:
        lines = file.readlines() + all_results
        urls = [line.strip() for line in lines if line.strip()]
        unique_urls = set(urls)
        file.seek(0)
        file.truncate()
        file.write('\n'.join(unique_urls))
