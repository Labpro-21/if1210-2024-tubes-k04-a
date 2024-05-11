import os
import time

if __package__ is None or __package__ == "":
    import assets
    from utils import clear
    import rgb
else:
    from .utils import clear
    from . import assets
    from . import rgb

WIDTH, HEIGHT = os.get_terminal_size()
W_WIDTH, W_HEIGHT = 100, 26
HBOR, VBOR = "═", "║"

def render_menu(header: list[str, bool], content_list: list[dict[str]], prompt: str) -> str:

    clear()

    # Left Padding
    lpad = " " * ((WIDTH - W_WIDTH) // 2)

    # Top Padding
    tpad = "\n" * 3  # ((HEIGHT - W_HEIGHT) // 2)

    # Render Top Padding
    print(tpad, end="")

    # Render Top Border
    print(lpad, end="")
    print("╔" + HBOR * (W_WIDTH - 2) + "╗")

    # Render Header
    if header:
        ascii_header = _parse_ascii(assets.ASCII[header[0]], (W_WIDTH - 2), "^")
        for line in ascii_header:
            print(lpad, end="")
            print(VBOR + line + VBOR)

        # Render Header Border
        if header[1]:
            print(lpad, end="")
            print("╠" + HBOR * (W_WIDTH - 2) + "╣")

    print(lpad, end="")
    print(VBOR + " " * (W_WIDTH - 2) + VBOR)

    # Render Contents 
    list_to_render = []
    temp = []
    temp_width = W_WIDTH - 2
    index = 0
    for content in content_list:
        if content["type"] == "ASCII":
            ascii = _parse_ascii(assets.ASCII[content['text']], content["width"], content["align"])
        elif content["type"] == "BUTTON":
            button_no = 0
            if content["isNumbered"]:
                index += 1
                button_no = index
            ascii = _parse_ascii(_generate_button_ascii(content["text"], content["inner_width"], content["inner_align"], button_no), content["width"], content["align"])

        elif content["type"] == "TEXT":
            if not content["width"]:
                content["width"] = W_WIDTH - 2
            if not content["max_length"]:
                content["max_length"] = W_WIDTH - 2
            ascii = _parse_text(content['text'], content['max_length'], content['align'], content['width'])
            

        if content["width"] > temp_width:
            list_to_render.append(temp)
            temp = []
            temp_width = W_WIDTH - 2
        
        temp.append((ascii, content["width"]))
        temp_width -= content["width"]

    list_to_render.append(temp)
    for asciis in list_to_render:
        maks = 0
        for ascii in asciis:
            maks = maks if len(ascii[0]) < maks else len(ascii[0])
            
        for i in range(maks):
            print(lpad, end="")
            print(VBOR, end="")
            sum = 0
            for ascii in asciis:
                sum += ascii[1]
                if i >= len(ascii[0]):
                    print(" " * ascii[1], end="")
                else:
                    print(ascii[0][i], end="")
            print(" " * (W_WIDTH - sum - 2) + VBOR)

    print(lpad, end="")
    print(VBOR + " " * (W_WIDTH - 2) + VBOR)

    # Render Bot Border
    print(lpad, end="")
    print("╚" + HBOR * (W_WIDTH - 2) + "╝")

    return input(lpad + " " + prompt)

def _generate_button_ascii(text: str, width: int, align: str, num: int) -> str:
    result = ""
    result += "┌" + "─" * (width - 2) + "┐" + "\n"
    content = "{text:{align}{width}}".format(text=text, align=align, width=width-2)
    content_list = [char for char in content]
    if num:
        content_list[1] = str(num)
        content_list[2] = "."
        content = ""
        for char in content_list:
            content += char
    result += "│" + content + "│" + "\n"
    result += "└" + "─" * (width - 2) + "┘"
    return result

def _parse_ascii(ascii: str, width: int, align: str) -> list[str]:
    result = []
    temp = ""
    for char in ascii:
        if char == "\n":
            result.append(temp)
            temp = ""
        else:
            temp += char
    if temp:
        result.append(temp)

    if result[0] == "BW":
        result = _encode_bw([line for i, line in enumerate(result) if i != 0], width, align)
    elif result[0] == "RGB":
        result = _encode_rgb([line for i, line in enumerate(result) if i != 0], width, align)
    else:
        result = _encode_text(result, width, align)

    return result

def _parse_text(text: str, width: int, align: str, w_width: int) -> list[str]:

    result = []
    
    if align == "*":
        for i in range(3):
            result.append(" " * w_width)

    temp = ""
    i = 0
    for char in text:
        if char == "\n":
            result.append(temp)
            i = 0
            temp = ""
        else:
            temp += char
            i += 1
        if i == width:
            result.append(temp)
            temp = ""
            i = 0
    if temp:
        result.append(temp)

    if align == "*":
        for i in range(3):
            result.append(" " * w_width)
        align = "^"

    result = _encode_text(result, w_width, align)
    return result

def _encode_text(arr: list[str], width: int, align: str) -> list[str]:
    for i in range(len(arr)):
        arr[i] = "{text: {align}{width}}".format(text=arr[i], align=align, width=width)
    return arr

def _encode_bw(arr: list[str], width:int, align: str) -> list[str]:
    code = {"0": " ", "1": "░", "2": "▒", "3": "▓", "4": "█"}
    keys = [key for key in code]
   

    result = []
    temp = ""
    for line in arr:
        for char in line:
            if char in keys:
                temp += code[char] * 2
            else:
                temp += char
        temp = "{text: {align}{width}}".format(text=temp, align=align, width=width) 
        result.append(temp)
        temp = ""

    return result

def _encode_rgb(arr: list[str], width:int, align:str) -> list[str]:
    code = {"C": (153, 76, 0), "B": (0, 167, 237), "Y": (255, 176, 46), "H": (0, 0, 0), "P": (255, 255, 255)}
    keys = [key for key in code]
    
    # Double the length first
    result = []
    temp = ""
    for line in arr:
        for char in line:
            temp += char * 2
        result.append(temp)
        temp = ""

    arr = result

    pixel = "█"
    empty = " "

    result = []
    temp = ""
    for line in arr:
        line = "{text: {align}{width}}".format(text=line, align=align, width=width) 
        for char in line:
            if char in keys:
                R, G, B = code[char]
                temp += f"{rgb.rgb_text(R, G, B)}{pixel}"
            else:
                temp += empty

        temp += "\033[0m"
        result.append(temp)
        temp = ""

    return result


if __name__ == "__main__":
    contents = [
        {"type": "ASCII", "text": "HALO_AGENT", "width": 60, "align": ">"},
        {"type": "ASCII", "text": "RGB_PERRY", "width": 38, "align": "^"},
        {"type": "TEXT", "text": "Test percobaan wkwkw", "width": 98, "align": "*", "max_length": 0},
        {"type": "BUTTON", "text": "REGISTER", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "LOGIN", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": False},
        ]
    res = render_menu(["TITLE", False], contents, "Sudahkah kamu sholat hari ini?(y/n) : ")
    print(res)
    buttons = [["REGISTER", 22, "^", 98, "^", True],
                ["LOGIN", 22, "^", 98, "^", True],
                ["EXIT", 22, "^", 98, "^", True],
               ]
    main_menu = render_menu(["TITLE", False], [], buttons, "", "Pilih menu yang ingin dibuka: ")
    print(main_menu)

