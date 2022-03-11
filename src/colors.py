valid_hex = "0123456789ABCDEF".__contains__


def cleanhex(data):
    return "".join(filter(valid_hex, data.upper()))


def print_hex(text, hexcode):
    hexint = int(cleanhex(hexcode), 16)
    print(
        "\x1B[38;2;{};{};{}m{}\x1B[0m".format(
            hexint >> 16, hexint >> 8 & 0xFF, hexint & 0xFF, text
        ),
        end="",
    )
