
import lib.tft_config as tft_config
import lib.vga1_8x16 as font

tft = tft_config.config(tft_config.WIDE)

tft.rotation(0)
tft.fill(0)

tft.text(
    font,
    f"Hello gamepad!",
    80, 200
)
tft.fill(0)

def show_gamepad(data, binary_data):
    tft.text(
        font,
        f"L-XY: {data[1], data[2]} ",
        10, 30
    )
    tft.text(
        font,
        f"R-XY: {data[3], data[4]} ",
        10, 60
    )
    tft.text(
        font,
        f"xaby: {bin((data[5] & 0b11110000) >> 4)}",
        10, 90
    )
    tft.text(
        font,
        f"dpad: {bin(data[5] & 0b00001111)}",
        10, 120
    )
    tft.text(
        font,
        f"other: {bin(data[6])}",
        10, 150
    )
    # tft.text(
    #     font,
    #     f"bin: {bin(int.from_bytes(binary_data, byteorder='big'))}",
    #     10, 40
    # )

if __name__ == "__main__":
    data = [1, 111,222, 112,221, 8,0, 6]
    show_gamepad(data)