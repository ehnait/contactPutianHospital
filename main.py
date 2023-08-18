from concurrent.futures import ThreadPoolExecutor
from DrissionPage import ChromiumPage, ChromiumOptions

# http://g1879.gitee.io/drissionpagedocs/ChromiumPage/browser_options/
co = ChromiumOptions()
# 不加载图片、无界面模式、超时时间
co.set_no_imgs(True).set_headless(True).set_timeouts(implicit=2).auto_port(True)
co.set_paths(browser_path=r'这里修改为您的浏览器可执行文件路径，可以在chrome浏览器的地址栏中输入：chrome://version 查看')
tel_number = '手机号码'


def iterate_api(file_path):
    page = ChromiumPage(addr_driver_opts=co)
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    with ThreadPoolExecutor(max_workers=32) as executor:
        success_count = 0
        cur_index = 1
        for tid in executor.map(page.new_tab, urls):
            try:
                new_tab = page.get_tab(tid)
                new_tab.wait.load_start()
                print(f"序号{cur_index} , 标题:{new_tab.title}")

                pass_mod_display = new_tab.ele('@class:passMod_dialog-wrapper passMod_show')
                if pass_mod_display:
                    new_tab.refresh()
                    new_tab.wait.load_complete()

                captcha_close_display = new_tab.ele('@class:imlp-component-captcha-close')
                if captcha_close_display:
                    captcha_close_display.click()

                leavetel_input = new_tab.ele('@class:leavetel-input')
                if not leavetel_input:
                    leave_tel = new_tab.ele('@class:pc-icon-leave-tel')
                    if leave_tel:
                        leave_tel.click()
                        leavetel_input = new_tab.ele('@class:leavetel-input')

                if leavetel_input:
                    leavetel_input.input(tel_number)
                    callback = new_tab.ele('@class:leavetel-callback')
                    if callback:
                        callback.click()
                    success_count += 1
                print(f"成功数量, {success_count}/{len(urls)}")
            except Exception as e:
                print(f"Exception：{str(e)}")
            finally:
                cur_index += 1
                if new_tab:
                    page.close_tabs(tabs_or_ids=new_tab)
    page.quit()


if __name__ == '__main__':
    if tel_number.isdigit():
        iterate_api('api.txt')
    else:
        print("请先输入手机号码")
