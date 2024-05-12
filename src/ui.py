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
            ascii = _parse_text(content['text'], content['width'], content['align'], content['max_length'], content['inner_align'])
        elif content ['type'] == "NEWLINE":
            ascii = [" " * (W_WIDTH - 2)]
            content['width'] = W_WIDTH - 2
        elif content ['type'] == "TABLE":
            ascii = _data_to_ascii_table(content['data'], content['width'], content['align'], content['inner_width'], content['inner_align'], content['size'])

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
    
    if prompt:
        return input(lpad + " " + prompt)
    return ""

def enter_to_continue_menu(message: str, button_message: str) -> bool:
    while True:
        contents = [
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {"type": "TEXT", "text": message, "width": 0, "align": "*", "max_length": 80, "inner_align": "^"},
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {"type": "BUTTON", "text": button_message, "inner_width": 22, "inner_align": "^", "width": 98, "align": "^", "isNumbered": False},
        ]

        user_inp = render_menu([], contents, "Tekan enter untuk melanjutkan ")
        break

    return

def confirm_menu(message: str) -> bool:
    isConfirm = False
    while True:
        contents = [
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {"type": "TEXT", "text": message, "width": 0, "align": "*", "max_length": 80, "inner_align": "^"},
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {'type': "NEWLINE"},
        {"type": "BUTTON", "text": "Ya", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        {"type": "BUTTON", "text": "Tidak", "inner_width": 22, "inner_align": "^", "width": 49, "align": "^", "isNumbered": True},
        ]

        user_inp = render_menu([], contents, "Masukkan pilihanmu disini: ")
        if user_inp == '1':
            isConfirm = True
            break
        if user_inp == '2':
            break

    return isConfirm

def _generate_button_ascii(text: str, width: int, align: str, num: int) -> str:
    result = ""
    result += "┌" + "─" * (width - 2) + "┐" + "\n"
    lines = []
    temp = ""
    i = 0
    for char in text:
        if char == "\n":
            temp = "│{text: {align}{width}}│".format(text=temp, align=align, width=width-2)
            lines.append(temp) 
            i = 0
            temp = ""
        else:
            temp += char
            i += 1
        if i == width - 2:
            temp = "│{text: {align}{width}}│".format(text=temp, align=align, width=width-2)
            lines.append(temp)
            temp = ""
            i = 0
    if temp:
        temp = "│{text: {align}{width}}│".format(text=temp, align=align, width=width-2)
        lines.append(temp)        
    
    first_line = [char for char in lines[0]]
    if num:
        first_line[2] = str(num)
        first_line[3] = "."
        content = ""
        for char in first_line:
            content += char
        lines[0] = content
    for line in lines:
        result += line
        result += "\n"
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

def _parse_text(text: str, width: int, align: str, max_width: int, inner_align: str) -> list[str]:
    result = []
    
    if align == "*":
        for i in range(3):
            result.append(" " * max_width)

    temp = ""
    i = 0
    for char in text:
        if char == "\n":
            temp = "{text: {align}{width}}".format(text=temp, align=inner_align, width=max_width)
            result.append(temp)
            i = 0
            temp = ""
        else:
            temp += char
            i += 1
        if i == max_width:
            temp = "{text: {align}{width}}".format(text=temp, align=inner_align, width=max_width)
            result.append(temp)
            temp = ""
            i = 0
    if temp:
        temp = "{text: {align}{width}}".format(text=temp, align=inner_align, width=max_width)
        result.append(temp)

    if align == "*":
        for i in range(3):
            result.append(" " * max_width)
        align = "^"

    result = _encode_text(result, width, align)
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

        temp += rgb.RESET
        result.append(temp)
        temp = ""

    return result


def _data_to_ascii_table(data: list[dict[str, str]], width:int, align: str, inner_width: int, inner_align: str,size: list[int] = []) -> list[str]:
    vbor, hbor, trbor, tlbor, tbor, tlcor, trcor, brcor, blcor, tdbor, tubor = "│", "─", "├", "┤", "┼", "┌", "┐", "┘", "└", "┬", "┴"
    width
    result = []
    
    if width == 0:
        width = W_WIDTH - 2

    keys = [key for key in data[0]]
    if not size:
        size = [(width - len(keys) - 1) // len(keys) for i in range(len(keys))]
    
    # Top border
    line = tlcor
    for j, length in enumerate(size):
        line += hbor * length
        if j != len(size) - 1:
            line += tdbor
    line += trcor
    result.append(line)

    # Column index
    column_index_parsed = _parse_table_line(keys, size, align)
    height = len(column_index_parsed[0])
    for _ in range(height):
        line = vbor
        for cell in column_index_parsed:
            line += cell[_] + vbor
        result.append(line)
    line = trbor
    for j, length in enumerate(size):
        line += hbor * length
        if j != len(size) - 1:
            line += tbor
    line += tlbor
    result.append(line)

    for i, row in enumerate(data):
        row_data = []
        for key in row:
            row_data.append(row[key])
        row_parsed = _parse_table_line(row_data, size, inner_align)
        height = len(row_parsed[0])
        for _ in range(height):
            line = vbor
            for cell in row_parsed:
                line += cell[_] + vbor
            result.append(line)

        if i != len(data) - 1:
            left_section = trbor
            mid_section = tbor
            right_section = tlbor
        else:
            left_section = blcor
            mid_section = tubor
            right_section = brcor
        line = left_section
        for j, length in enumerate(size):
            line += hbor * length
            if j != len(size) - 1:
                line += mid_section
        line += right_section
        result.append(line)

    for i, row in enumerate(result):
        result[i] = "{text: {align}{width}}".format(text=row, align=align, width=width)

    return result

    
def _parse_table_line(data_list: list[str], size: list[int], align: str):
    result = []
    max_height = 1

    # Search for max height of a cell
    for i, value in enumerate(data_list):
        value = str(value)
        height = int(len(value) / (size[i] - 2) + 0.9999)
        max_height = height if height > max_height else max_height
    
    for i, value in enumerate(data_list):
        value = str(value)
        cell = []
        temp = " "
        j = 0
        for char in value:
            if j == size[i] - 2:
                cell.append(temp + " ")
                temp = " "
                j = 1
                temp += char
            else:
                temp += char
                j += 1
        if temp:
            temp = "{text: {align}{width}} ".format(text=temp, align=align, width=size[i] - 1)
        cell.append(temp)
        remainder = max_height - len(cell)

        if remainder > 0:
            for k in range(remainder):
                cell.append(" " * size[i])
        result.append(cell)

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
