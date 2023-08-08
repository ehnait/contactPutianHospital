from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess


def run_main():
    # 使用 subprocess 模块执行 main.py 文件
    subprocess.run(["python", "main.py"])


# 创建调度器对象
scheduler = BlockingScheduler()

# 添加一个每天早上 9 点触发运行的定时任务
scheduler.add_job(run_main, 'cron', hour=9)

# 启动调度器，并等待程序退出信号（例如键盘中断）
try:
    scheduler.start()
except KeyboardInterrupt:
    pass
