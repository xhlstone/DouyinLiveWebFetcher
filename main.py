import threading
import traceback
from liveMan import DouyinLiveWebFetcher, get_logger


def monitor_live_room(_live_id):
    """
    单个直播间的监控任务（线程执行的核心函数）
    """
    logger = get_logger(_live_id)
    try:
        # 初始化直播间抓取器并执行任务
        room = DouyinLiveWebFetcher(_live_id, logger)
        room.get_room_status()
        room.start()  # 假设 start() 是阻塞式任务（如持续监控），若非阻塞可按需调整
    except Exception as e:
        # 捕获线程内异常并记录
        logger.error(f"直播间执行报错, {_live_id}: {str(e)}")
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    live_ids = [
        "294530521082",
        "646454278948",
        "345350598855",
        "186331227245",
        "349657363582",
        "23968056366",
        "252389686228",
        "11858974839",
        "220506899033",
        "589959159975",
        "932476672609",
        "719136762870",
        "604149758091",
        "599675992849",
        "4874232505",
        "139028859310",
        "35355979057",
        "62154220363",
        "310539894467",
        "282430486196",
        "959823974763",
        "372258197395",
    ]

    # 1. 创建线程列表，存储所有线程对象
    threads = []
    for live_id in live_ids:
        # 创建线程，指定目标函数和参数
        t = threading.Thread(
            target=monitor_live_room,  # 线程要执行的函数
            args=(live_id,)  # 传递给函数的参数（元组形式，单个参数需加逗号）
        )
        threads.append(t)
        # 设置为守护线程（可选）：主程序退出时自动终止所有子线程
        t.daemon = True

    # 2. 启动所有线程
    for t in threads:
        t.start()
        # 可选：轻微延迟避免瞬间创建过多线程（视任务特性调整）
        # time.sleep(0.1)

    # 3. 等待所有线程执行完成（关键）
    # 若不等待，主程序会直接退出，子线程也会被终止
    for t in threads:
        t.join()

    print("所有直播间监控任务已结束")
