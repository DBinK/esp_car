
import time
import json
import struct
import espnow
import network


time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上


# 初始化 WiFi 和 espnow
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()  # 因为 ESP8266 会自动连接到最后一个接入点

now = espnow.ESPNow()
now.active(True)  # 连接dk广播地址
now.add_peer(b"\xff\xff\xff\xff\xff\xff")



def read_espnow():
    """读取espnow数据并进行解包处理"""
    host, msg = now.recv(5)  # 读取所有可用的数据, 参数: 超时时间ms

    print("espnow数据:", msg)

    if msg is None:  # 如果没有数据，则返回
        return [1, 0, 0, 0, 0, 8, 0, 6]
    
    else:
        # 假设 msg 是字节串，需要先解码为字符串
        msg_str = msg.decode('utf-8')
        data = json.loads(msg_str)  # 处理接收到的数据
        return data


if __name__ == "__main__":
    print("正在读取espnow数据...")
    while True:
        data = read_espnow()
        print(data)
        time.sleep(0.1)