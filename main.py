import random
import time
from concurrent.futures import ThreadPoolExecutor

from DrissionPage import ChromiumPage, ChromiumOptions

# http://g1879.gitee.io/drissionpagedocs/ChromiumPage/browser_options/
co = ChromiumOptions()
# 不加载图片、有界面模式、自动获取端口
co.set_no_imgs(True).set_headless(False).auto_port(True)

co.set_paths(browser_path=r'这里修改为您的浏览器可执行文件路径，可以在chrome浏览器的地址栏中输入：chrome://version 查看')
tel_number = '手机号码'


def process_tab(page, url):
    time.sleep(random.uniform(0, 3))  # 自己权衡是否需要延迟
    """
      处理网页标签
        - 使用 page.new_tab(url) 创建新的标签页，返回标签页 ID（tid）
        - 获取页面上指定 ID 的标签页（tab）对象
        - 等待页面加载完成后再处理该标签页
        - 检查再次是否存在类名为 "pc-icon-leave-tel" 的元素（离开电话图标）
            - 若存在，则点击离开电话图标，并在 "leavetel-input" 元素中输入电话号码
        - 检查类名为 "leavetel-callback" 的元素（回拨按钮）
            - 若存在，则点击回拨按钮，并返回字典对象：{"state": True, "title": tab.title}
      :param page: ChromiumPage对象，用于管理和操作浏览器标签页
      :param url: 网页地址
      :return: 字典，包含处理结果状态和标题信息
      """

    tab = None
    try:
        tid = page.new_tab(url)
        tab = page.get_tab(tid)
        tab.wait.load_start()

        icon_leave_tel = tab.ele('@class:pc-icon-leave-tel')
        if icon_leave_tel:
            icon_leave_tel.click(by_js=True)
            leavetel_input = tab.ele('@class:leavetel-input')
            leavetel_input.input(tel_number)
            callback = tab.ele('@class:leavetel-callback')
            if callback:
                callback.click(by_js=True)
                return {"state": True, "title": tab.title}


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if tab:
            page.close_tabs(tabs_or_ids=tab)


def iterate_api(file_path, workers=4):
    """
    迭代处理API
      - 使用 ChromiumPage 创建浏览器页面对象（page）
      - 读取文件中的所有 URL，并计算总长度（total_len）
      - 使用 split_list 函数将 URL 列表拆分成多个子列表，每个子列表最大长度为4
      - 初始化成功计数器 success_count
      - 遍历每个子列表，使用线程池并发执行 process_tab 函数，并通过 map 获取结果
      - 如果返回结果不为空，则获取状态和标题，并根据状态更新成功计数器和打印输出信息
    :param file_path: API文件路径

    """
    page = ChromiumPage(addr_driver_opts=co)
    page.get('https://www.baidu.com/')
    time.sleep(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
        total_len = len(urls)

    success_count = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for result in executor.map(lambda url: process_tab(page, url), urls):
            if result:
                state = result["state"]
                title = result["title"]
                if state:
                    success_count += 1
                    print(f"成功数量, {success_count}/{total_len} ,标题:{title}")


if __name__ == '__main__':
    if tel_number.isdigit():
        start_time = time.time()
        iterate_api('api.txt')
        end_time = time.time()
        print(f"结束！总耗时: {end_time - start_time} seconds")

    else:
        print("请先输入手机号码")
