
import lib.tft_config as tft_config
import lib.vga1_8x16 as font

tft = tft_config.config(tft_config.WIDE)

tft.rotation(0)
tft.fill(0)

tft.text(
    font,
    f"Hello gamepad!",
    10, 10
)

def show_gamepad(data, binary_data):
    tft.text(
        font,
        f"raw: {data} ",
        10, 10
    )
    # tft.text(
    #     font,
    #     f"bin: {bin(int.from_bytes(binary_data, byteorder='big'))}",
    #     10, 40
    # )
    tft.text(
        font,
        f"xaby: {bin((data[5] & 0b11110000) >> 4)}",
        10, 40
    )
    tft.text(
        font,
        f"other: {bin(data[6])}",
        10, 70
    )
    tft.text(
        font,
        f"dpad: {bin(data[5] & 0b00001111)}",
        10, 100
    )

if __name__ == "__main__":
    data = [1, 111,222, 112,221, 8,0, 6]
    show_gamepad(data)