from concurrent.futures import ThreadPoolExecutor
from DrissionPage import ChromiumPage, ChromiumOptions
import requests

# http://g1879.gitee.io/drissionpagedocs/ChromiumPage/browser_options/
co = ChromiumOptions()
# 不加载图片、有界面模式、超时时间、自动获取端口
co.set_no_imgs(True).set_headless(False).set_timeouts(implicit=2).auto_port(True)

# 是否开启多线程多Tab标签模式
IS_ENABLE_MULTI_TAB = False
co.set_paths(browser_path=r'这里修改为您的浏览器可执行文件路径，可以在chrome浏览器的地址栏中输入：chrome://version 查看')
tel_number = '手机号码'


def check_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查响应状态码是否为200
        # print("URL is accessible")
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


def process_tab(page):
    pass_mod_display = page.ele('@class:passMod_dialog-wrapper passMod_show')
    if pass_mod_display:
        page.refresh()
        page.wait.load_complete()

    captcha_close_display = page.ele('@class:imlp-component-captcha-close')
    if captcha_close_display:
        captcha_close_display.click()

    leavetel_input = page.ele('@class:leavetel-input')
    if not leavetel_input:
        leave_tel = page.ele('@class:pc-icon-leave-tel')
        if leave_tel:
            leave_tel.click()
            leavetel_input = page.ele('@class:leavetel-input')

    if leavetel_input:
        leavetel_input.input(tel_number)
        callback = page.ele('@class:leavetel-callback')
        if callback:
            callback.click()


def iterate_api(file_path):
    page = ChromiumPage(addr_driver_opts=co)

    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    success_count = 0
    if IS_ENABLE_MULTI_TAB:
        with ThreadPoolExecutor() as executor:
            cur_index = 1
            for tid in executor.map(page.new_tab, urls):
                try:
                    new_tab = page.get_tab(tid)
                    new_tab.wait.load_start()
                    print(f"序号{cur_index} , 标题:{new_tab.title}")
                    process_tab(new_tab)
                    success_count += 1
                    print(f"成功数量, {success_count}/{len(urls)}")
                except Exception as e:
                    print(f"Exception：{str(e)}")
                finally:
                    cur_index += 1
                    if new_tab:
                        page.close_tabs(tabs_or_ids=new_tab)

        page.quit()
    else:
        try:
            for url in urls:
                accessible = check_url(url)
                if accessible:
                    page.get(url)
                    process_tab(page)
                    success_count += 1
                    print(f"成功数量, {success_count}/{len(urls)}")
        except Exception as e:
            print(f"Exception：{str(e)}")
        finally:
            page.quit()


if __name__ == '__main__':
    if tel_number.isdigit():
        iterate_api('api.txt')
    else:
        print("请先输入手机号码")
