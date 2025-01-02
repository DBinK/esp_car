# 标准库
import time
import json
import network
import asyncio
import espnow
from machine import Pin, ADC, Timer

# 本地库
import modules.gamepad as gamepad
import modules.lcd as lcd
from modules.utils import debounce, TimeDiff

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上

# 初始化 wifi
sta = network.WLAN(network.STA_IF)  # 或者使用 network.AP_IF
sta.active(True)
sta.disconnect()  # 对于 ESP8266

# 初始化 espnow
now = espnow.ESPNow()
now.active(True)
peer = b"\xff\xff\xff\xff\xff\xff"  # 使用广播地址
now.add_peer(peer)

# 构建手柄对象
gamepad = gamepad.Gamepad()
main_dt = TimeDiff()

gamepad_data = []
binary_data  = gamepad.read_bin()

def data_to_json(data):
    data_dict = {
        "ID": data[0],
        "LX": data[1],
        "LY": data[2],
        "RX": data[3],
        "RY": data[4],
        "XABY/Pad": data[5],
        "LS/RS/Start/Back": data[6],
        "mode": data[7],
    }
    
    print(data_dict)
    
    return json.dumps(data_dict)


async def show_lcd():
    global binary_data, gamepad_data

    while True:
        binary_str = hex(int.from_bytes(binary_data, 'big'))

        lcd.show_gamepad(gamepad_data, binary_str)   # 在lcd显示数据

        await asyncio.sleep(0.1) 

async def send_espnow():
    global binary_data, gamepad_data, peer

    while True:
        binary_data  = gamepad.read_bin()
        gamepad_data = gamepad.data

        # data_json = data_to_json(data)  # 将数据转换为 JSON 字符串并发送

        data_json = json.dumps(gamepad_data)      # 将列表直接转换为 JSON 字符串

        now.send(peer, data_json) 

        print(f"发送数据: {gamepad_data}") 

        diff = main_dt.time_diff() 
        
        print(f"延迟ms: {diff / 1000_000}, 频率Hz: {1_000_000_000 / diff}")
        
        await asyncio.sleep(0.001) 


async def main():
    await asyncio.gather(
        send_espnow(),  # 启动读取 espnow 的任务
        show_lcd(),     # 启动显示 lcd 的任务
    )

# 运行主协程
asyncio.run(main())