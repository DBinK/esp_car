# 标准库
import time
import json
import network
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


def main(tim_callback):

    data_bin = gamepad.read_bin()
    data = gamepad.data
    
    lcd.show_gamepad(data, data_bin)  # 在lcd显示数据

    data_json = data_to_json(data)  # 将数据转换为 JSON 字符串并发送

    # data_json = json.dumps(data)  # 将列表直接转换为 JSON 字符串

    now.send(peer, data_json)

    print(f"发送数据: {data_json}")

    diff = main_dt.time_diff()
    
    print(f"延迟ms: {diff / 1000_000}, 频率Hz: {1_000_000_000 / diff}")


# 开启定时器
tim = Timer(1)

@debounce(100_000_000)
def stop_btn_callback(pin):
    if pin.value() == 0:
        tim.deinit()
        print("停止定时器")  # 不然Thonny无法停止程序


stop_btn = Pin(0, Pin.IN, Pin.PULL_UP)
stop_btn.irq(stop_btn_callback, Pin.IRQ_FALLING)

tim.init(period=100, mode=Timer.PERIODIC, callback=main)
