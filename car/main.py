import struct
import time
import asyncio
import espnow
import network
from machine import Pin

from car.modules.motion import RobotController

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上


# 初始化 Omni Bot
robot = RobotController()

# 初始化 LED
led = Pin(15, Pin.OUT, value=1)

# 初始化 WiFi 和 espnow
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()  # 因为 ESP8266 会自动连接到最后一个接入点

now = espnow.ESPNow()
now.active(True)  # 连接dk广播地址
now.add_peer(b"\xff\xff\xff\xff\xff\xff")

# 初始化停止按钮
def stop_btn_callback(pin):
    global sw
    time.sleep(0.1)
    if pin.value() == 0:
        sw = not sw
        led.value(not led.value())
        print("停止定时器")  # 不然Thonny无法停止程序


stop_btn = Pin(0, Pin.IN, Pin.PULL_UP)
stop_btn.irq(stop_btn_callback, Pin.IRQ_FALLING)


async def read_espnow():
    """读取espnow数据并进行解包处理"""
    while True:
        # print("正在读取espnow数据...")
        host, msg = now.recv()  # 读取所有可用的数据
        process_espnow_data(msg)  # 处理接收到的数据

        await asyncio.sleep(0.001)  # 等待一段时间再检查


def process_espnow_data(msg):
    pass


def process_uart_data(data):
    # 检查数据长度
    # 解包数据
    try:
        pass

    except Exception as e:
        print(f"解包数据时出错: {e}")


async def main():
    await asyncio.gather(
        # read_uart(),   # 启动读取 UART 的任务
        read_espnow(),  # 启动读取 espnow 的任务
    )


# 运行主协程
asyncio.run(main())

