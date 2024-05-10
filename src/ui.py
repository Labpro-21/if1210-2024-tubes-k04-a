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

def render_menu(header: list[str, bool], ascii_list: list[list[str, int, str]], buttons: list[list[str, int, str, int, str, bool]], text_content: list[str, int, str, int], prompt: str) -> str:

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
    ascii_header = _parse_ascii(assets.ASCII[header[0]], (W_WIDTH - 2), "^")
    for line in ascii_header:
        print(lpad, end="")
        print(VBOR + line + VBOR)

    # Render Header Border
    if header[1]:
        print(lpad, end="")
        print("╠" + HBOR * (W_WIDTH - 2) + "╣")

    # Render ASCII arts
    list_to_render = []
    temp = []
    temp_width = W_WIDTH - 2
    for ascii_data in ascii_list:
        ascii = _parse_ascii(assets.ASCII[ascii_data[0]], ascii_data[1], ascii_data[2])

        if ascii_data[1] > temp_width:
            list_to_render.append(temp)
            temp = []
            temp_width = W_WIDTH - 2
        
        temp.append((ascii, ascii_data[1]))
        temp_width -= ascii_data[1]

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
    """
    for ascii_data in ascii_list:
        ascii = _parse_ascii(assets.ASCII[ascii_data[0]], ascii_data[1] - 2, ascii_data[2])
        for line in ascii:
            print(lpad, end="")
            print("│" + line + " " * (W_WIDTH - 2 -len(line)) + "│")
    """
    

    # Render text
    if text_content:
        print(lpad, end="")
        print(VBOR + " " * (W_WIDTH - 2) + VBOR)
        text = _parse_text(text_content[0], text_content[1], text_content[2], text_content[3])
        for line in text:
            print(lpad, end="")
            print(VBOR + line + " " * (W_WIDTH - 2 - len(line)) + VBOR)
        print(lpad, end="")
        print(VBOR + " " * (W_WIDTH - 2) + VBOR)

    
    # Render buttons
    """
    if buttons:
        print(lpad, end="")
        print(VBOR + " " * (W_WIDTH - 2) + VBOR)
        index = 1
        for button in buttons:
            button_no = 0
            if button[5]:
                button_no = index
                index += 1
            ascii = _parse_ascii(_generate_button_ascii(button[0], button[1], button[2], button_no), button[3], button[4])
            for line in ascii:
                print(lpad, end="")
                print(VBOR + line + " " * (W_WIDTH - 2 - len(line)) + VBOR)
        print(lpad, end= "")
        print(VBOR + " " * (W_WIDTH - 2) + VBOR)
    """ 
    button_to_render = []
    temp = []
    temp_width = W_WIDTH - 2
    index = 1
    for button in buttons:
        button_no = 0
        if button[5]:
            button_no = index
            index += 1
        ascii = _parse_ascii(_generate_button_ascii(button[0], button[1], button[2], button_no), button[3], button[4])

        if button[3] > temp_width:
            button_to_render.append(temp)
            temp = []
            temp_width = W_WIDTH - 2
        
        temp.append((ascii, button[3]))
        temp_width -= button[3]

    button_to_render.append(temp)

    if button_to_render:
        print(lpad, end="")
        print(VBOR + " " * (W_WIDTH - 2) + VBOR)

    for asciis in button_to_render:
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
    
    if button_to_render:
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
    if not width:
        width = W_WIDTH - 2
    if not w_width:
        w_width = W_WIDTH - 2

    result = []
    
    if align == "*":
        for i in range(3):
            result.append("")

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
            result.append("")
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
    res = render_menu(["TITLE", False], [["HALO_AGENT", 60, ">"], ["RGB_PERRY", 38, "^"]], [], "", "Sudahkah kamu sholat hari ini?(y/n) : ")
    print(res)
    buttons = [["REGISTER", 22, "^", 98, "^", True],
                ["LOGIN", 22, "^", 98, "^", True],
                ["EXIT", 22, "^", 98, "^", True],
               ]
    main_menu = render_menu(["TITLE", False], [], buttons, "", "Pilih menu yang ingin dibuka: ")
    print(main_menu)
