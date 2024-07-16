import time
import random
from collections import Counter
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from DrissionPage import ChromiumPage, ChromiumOptions

# http://g1879.gitee.io/drissionpagedocs/ChromiumPage/browser_options/
co = (ChromiumOptions()
.set_no_imgs(False)  # 加载图片
.set_headless(False)  # 有界面模式
.auto_port(True)  # 自动获取端口
# .set_proxy("xxxxx")
.set_user_agent(UserAgent().random)  # 随机UserAgent
.set_paths(
    browser_path=r'这里修改为您的浏览器可执行文件路径，可以在chrome浏览器的地址栏中输入：chrome://version 查看'))
BAIDU_URL = 'https://www.baidu.com/'
TEL_NUMBER = ''  # 手机号码
TEL_NAME = ''  # 名字(可选)
# TEL_TEXT = ''  # 留言(可选)
ENABLE_OTP = False  # 如果为True ,且页面元素存在‘去官网按钮’则进入官网发送验证码 https://github.com/ehnait/contactPutianHospital/issues/13

# def process_tab(page, url, success_counter, total_len):
#     """
#     处理网页标签函数
#     - 创建新的标签页（tid）并获取标签页对象（tab）
#     - 等待标签页加载开始
#     - 检查标签页上是否存在指定的元素（icon_leave_message）
#     - 如果存在，则点击该元素，并在相应的输入框元素中输入电话号码和姓名（如果有）
#     - 检查是否存在指定的元素（callback）
#     - 如果存在，则点击该元素，并返回标签页标题
#     - 如果启用了验证码功能，并且存在指定的元素（go_official_website），则点击该元素，并等待新页面加载开始
#     - 检查该标签页是否存在指定的 iframe 元素（consult_card）
#     - 如果存在，则点击该元素（consult_card），并输入手机号码和点击获取验证码
#     - 最后关闭标签页并输出log
#     :param page: ChromiumPage对象，用于管理和操作浏览器标签页
#     :param url: 网页地址
#     :param success_counter: 计数器对象
#     :param total_len:
#     """
#     tab = None
#     tab_title = None
#     try:
#         tid = page.new_tab(url)
#         tab = page.get_tab(tid)
#         tab.wait.load_start()
#
#         icon_leave_message = tab.ele('@class:pc-icon-leave-message')
#         if icon_leave_message:
#             icon_leave_message.click(by_js=True)
#             leavetel_input = tab.ele('@class:tel-input ')
#             leavetel_input.input(TEL_NUMBER)
#             if TEL_NAME:
#                 name_input = tab.ele('@class:name-input')
#                 name_input.input(TEL_NAME)
#             if TEL_TEXT:
#                 text_input = tab.ele('@class:leaveword-textarea')
#                 text_input.input(TEL_TEXT)
#             callback = tab.ele('@class:leaveword-submit')
#             if callback:
#                 callback.click(by_js=True)
#                 tab_title = tab.title
#             if ENABLE_OTP:
#                 go_official_website = tab.ele('text:去官网')
#                 if go_official_website.click(by_js=True):
#                     page.wait.new_tab()  # 等待新标签页出现
#                     official_tab = page.get_tab(page.latest_tab)  # 获取新标签页对象
#                     iframe = official_tab.get_frame(1)  # 获取iframe对象
#                     consult_card = iframe('极速预约')
#                     if consult_card:
#                         consult_card.click(by_js=True)
#                         sjh_form_input = iframe(
#                             '@class=with-placeholder sjh-form-input sjh-form-input-tel hide-date-editing')
#                         sjh_form_input.input(TEL_NUMBER)
#                         sjh_captcha = iframe('获取验证码')
#                         sjh_captcha.click(by_js=True)
#                     page.close_tabs(tabs_or_ids=official_tab)
#     except Exception as e:
#         print(f"An error occurred: {e} , url: {url}")
#     finally:
#         if tab:
#             time.sleep(0.5)  # 自己权衡是否需要延迟
#             page.close_tabs(tabs_or_ids=tab)
#             if tab_title:
#                 success_counter.update([tab_title])
#                 print(f"留言成功数量, {len(success_counter)}/{total_len} ,标题:{tab_title}")





# 定义医生和护士的称谓
titles = ["医生", "护士", "主任", "医师", "院长", "专家", "同志","大夫"]

# 定义亲属的称谓
relatives = [
    "我的外公", "我的外婆", "我的父亲", "我的母亲",
    "我的哥哥", "我的姐姐", "我的弟弟", "我的妹妹",
    "我的表兄弟", "我的表姐妹", "我的堂兄弟", "我的堂姐妹",
    "我老婆", "我丈夫", "我妻子", "我的妻子",
    "我自己", "我本人", "我大姨", "我小姨",
    "我的大姑子", "我的小姑子", "我的大舅子", "我的小舅子"
]

# 定义更丰富的不同情况描述
situations = [
    "有一些毛病", "需要帮助", "需要您的帮助",
    "需要医疗建议", "需要治疗", "需要紧急处理",
    "有紧急情况", "需要进行检查", "需要手术治疗",
    "生病了", "情况不太好", "需要紧急救治",
    "需要安排手术", "需要进一步诊断"
]

# 更丰富的联系方式描述
contact_methods = [
    "我急需帮助，请尽快联系我 {number}",
    "有事找你，麻烦联系我 {number}",
    "情况紧急，请求帮助，请立即拨打 {number}",
    "需要紧急救助，请马上联系我 {number}",
    "我的病情急需处理，请尽快联系 {number}",
    "需要安排紧急手术，请与我联系 {number}",
    "有重要情况需要讨论，请拨打 {number} 联系我",
    "我有紧急问题，希望能与你通话 {number}",
    "请尽快与我联系，电话号码是 {number}",
    "通过 {number} 联系我",
    "请联系 {number}",
    "可以通过 {number} 找到我",
    "请拨打 {number}",
    "有急事，请立即拨打 {number}",
    "需要紧急帮助，请马上拨打 {number}",
    "需要紧急医疗服务，请联系 {number}",
    "有重要事项需要沟通，请拨打 {number}",
    "需要迅速安排治疗，请联系 {number}",
    "请随时与我联系，电话号码是 {number}",
    "请拨打 {number}"
]

# 更丰富的打招呼方式
greetings = [
    "您好", "你好", "hello", "hi", "HI", "Hello",
    "早上好", "下午好", "晚上好", "Hi there", "Hey"
]

def process_tab(page, url, success_counter, total_len):
    """
    处理网页标签函数
    - 创建新的标签页（tid）并获取标签页对象（tab）
    - 等待标签页加载开始
    - 检查标签页上是否存在指定的元素（icon_leave_message）
    - 如果存在，则点击该元素，并在相应的输入框元素中输入电话号码和姓名（如果有）
    - 检查是否存在指定的元素（callback）
    - 如果存在，则点击该元素，并返回标签页标题
    - 如果启用了验证码功能，并且存在指定的元素（go_official_website），则点击该元素，并等待新页面加载开始
    - 检查该标签页是否存在指定的 iframe 元素（consult_card）
    - 如果存在，则点击该元素（consult_card），并输入手机号码和点击获取验证码
    - 最后关闭标签页并输出log
    :param page: ChromiumPage对象，用于管理和操作浏览器标签页
    :param url: 网页地址
    :param success_counter: 计数器对象
    :param total_len:
    """
    tab = None
    tab_title = None
    try:
        tid = page.new_tab(url)
        tab = page.get_tab(tid)
        tab.wait.load_start()

        component_input = tab.ele('@class:imlp-component-typebox-input pc-imlp-component-typebox-input')
        if component_input:
            # 随机选择一条打招呼用语模板
            title = random.choice(titles)
            relative = random.choice(relatives)
            situation = random.choice(situations)
            contact_method_template = random.choice(contact_methods)
            # 替换模板中的 {number} 为实际的电话号码 TEL_NUMBER
            contact_method = contact_method_template.replace("{number}", TEL_NUMBER)
            # 随机选择一个打招呼方式
            greeting = random.choice(greetings)

            # 生成打招呼用语
            template = f"{greeting}{title}，{relative} {TEL_NAME} {situation}，{contact_method}。"
            print(template)


            component_input.input(template)
            send = tab.ele('@class:imlp-component-typebox-send-btn pc-imlp-component-typebox-send ')
            if send:
                send.click(by_js=True)

    except Exception as e:
        print(f"An error occurred: {e} , url: {url}")
    finally:
        if tab:
            time.sleep(0.5)  # 自己权衡是否需要延迟
            page.close_tabs(tabs_or_ids=tab)
            if tab_title:
                success_counter.update([tab_title])
                print(f"留言成功数量, {len(success_counter)}/{total_len} ,标题:{tab_title}")


def iterate_api(file_path):
    """
    迭代处理API函数
    - 创建 ChromiumPage 对象（page）用于管理和操作浏览器标签页
    - 打开百度页面并等待加载开始
    - 读取文件中的所有 URL，并计算总长度（total_len）
    - 初始化成功计数器 success_count
    - 如果开启ENABLE_OTP则循环遍历执行 process_tab 函数，否则使用线程池并发执行 process_tab 函数
    :param file_path: API文件路径
    """

    page = ChromiumPage(addr_driver_opts=co)
    page.get(BAIDU_URL)
    page.wait.load_start()
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = file.readlines()
        total_len = len(urls)
        random.shuffle(urls)  # 随机打乱列表元素顺序
    success_counter = Counter()
    if ENABLE_OTP:
        for url in urls:
            process_tab(page, url, success_counter, total_len)
    else:
        max_workers = 1  # 最大线程数
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(lambda url: process_tab(page, url, success_counter, total_len), urls):
                pass


if __name__ == '__main__':
    if TEL_NUMBER.isdigit():
        start_time = time.time()
        iterate_api('api.txt')
        end_time = time.time()
        print(f"结束！总耗时: {end_time - start_time} seconds")
    else:
        print("请先输入手机号码")
