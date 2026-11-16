import struct
import zlib


def make_png(size, path):
    bg, circle, fg = (31, 42, 68), (59, 76, 122), (255, 196, 0)
    cx = cy = size / 2
    r = size * 0.32
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            inside = (x - cx) ** 2 + (y - cy) ** 2 <= r * r
            tx = (x - (cx - r * 0.35)) / (r * 1.1)
            ty = abs(y - cy) / (r * 0.75)
            triangle = 0 <= tx <= 1 and ty <= 1 - tx
            color = fg if (triangle and inside) else circle if inside else bg
            row += bytes(color)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(tag, data):
        body = struct.pack(">I", len(data)) + tag + data
        return body + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)


make_icons = [(192, "public/icons/icon-192.png"), (512, "public/icons/icon-512.png")]
for size, path in make_icons:
    make_png(size, path)
print("Иконки созданы")