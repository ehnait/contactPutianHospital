from DrissionPage.easy_set import use_auto_port, set_no_imgs, set_headless, set_paths

tel_number = '输入目标号码'

if __name__ == '__main__':
    # 使用自动分配的端口和临时文件夹
    use_auto_port(True)
    # 禁止加载图像
    set_no_imgs(True)
    # 设置无头模式
    set_headless(False)
    # 设置你的浏览器路径
    # see: http://g1879.gitee.io/drissionpagedocs/get_start/before_start/
    set_paths(browser_path=r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
