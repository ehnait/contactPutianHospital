from config import tel_number
from concurrent.futures import ThreadPoolExecutor
from DrissionPage import ChromiumPage


def iterate_api(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        total_urls_count = len(urls)

        success_count = 0

        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = []

            for i, url in enumerate(urls):
                future = executor.submit(send_tel, ChromiumPage(), url)
                futures.append(future)

            for future in futures:
                if future.result():
                    success_count += 1

    print(f"总共成功：{success_count}/{total_urls_count}")


def send_tel(page, url):
    try:
        page.get(url, retry=1, interval=1, timeout=5)

        pass_mod_display = page.wait.ele_display('@class:passMod_dialog-wrapper passMod_show', timeout=1.5)
        if pass_mod_display:
            page.refresh()

        captcha_close_display = page.wait.ele_display('.imlp-component-captcha-close', timeout=0.5)
        if captcha_close_display:
            page.ele('.imlp-component-captcha-close').click()

        page.ele('@class:pc-icon-leave-tel', timeout=1).click()
        input_display = page.wait.ele_display('.leavetel-input ', timeout=3)
        if input_display:
            page.ele('.leavetel-input ').input(tel_number)
            page.ele('.leavetel-callback').click()
            return True

    except Exception as e:
        print(f"发生异常：{str(e)}  {url}")
    finally:
        page.quit()
        pass


if __name__ == '__main__':
    if tel_number.isdigit():
        iterate_api('api.txt')
    else:
        print("请先在文件config.py中配置手机号码")
