from PIL import Image
from itertools import chain

# with open("18_test_a.png", mode="b+r") as img:
#     b = img.read()
#     bitstr = bin(int(b.hex(), base=16))

img_a = Image.open("18_eval_a.png")
img_b = Image.open("18_eval_b.png")


HEADER = 2
SIXTEEN_BITS = 16
SIZE = 8


def img_lsbs(img: Image.Image) -> str:
    r, g, b = img.getdata(0), img.getdata(1), img.getdata(2)
    r, g, b = list(r), list(g), list(b)

    r_lsb, g_lsb, b_lsb = (
        [bin(p)[-1] for p in r],
        [bin(p)[-1] for p in g],
        [bin(p)[-1] for p in b],
    )

    lsbs = zip(*(r_lsb, g_lsb, b_lsb))
    lsbs_flat = list(chain.from_iterable(lsbs))
    lsbs_str = "".join(lsbs_flat)

    return lsbs_str


def lsbs_msg(lsbs_str: str) -> str:
    lsbs_header, lsbs_msg_size, lsbs_msg = (
        lsbs_str[:HEADER],
        lsbs_str[HEADER : HEADER + SIXTEEN_BITS],
        lsbs_str[HEADER + SIXTEEN_BITS :],
    )
    msg_size = int(lsbs_msg_size, 2) // 8

    txt = ""
    for i in range(0, len(lsbs_msg), SIZE):
        binary = lsbs_msg[i : i + SIZE]
        char = chr(int(binary, 2))
        txt += char

    return txt[:msg_size]


def lsbs_img(lsbs_str: str) -> Image.Image:
    print(lsbs_str[: HEADER + 2 * SIXTEEN_BITS])
    lsbs_header, lsbs_width, lsbs_height, lsbs_pixels = (
        lsbs_str[:HEADER],
        lsbs_str[HEADER : HEADER + SIXTEEN_BITS],
        lsbs_str[HEADER + SIXTEEN_BITS : HEADER + 2 * SIXTEEN_BITS],
        lsbs_str[HEADER + 2 * SIXTEEN_BITS :],
    )

    width = int(lsbs_width, 2)
    height = int(lsbs_height, 2)

    pixels = [int(p) * 255 for p in lsbs_pixels[: width * height]]
    pixels = bytes(pixels)

    img_out = Image.frombytes("L", (width, height), pixels)

    return img_out


print(lsbs_msg(img_lsbs(img_a)))
lsbs_img(img_lsbs(img_b)).show()
