if __name__ == "__main__":
    import file_io
else:
    from . import file_io

def save(save_folder: str, GAME_STATE: dict[str, str]) -> str:
    file_names = ["monster_inventory",
                  "item_inventory",
                  "monster_shop",
                  "item_shop",
                  "user_list",
                  ]
    keys = [key for key in GAME_STATE]

    for file in file_names:
        if not file in keys:
            return "failed"
    
    for file in file_names:
        key = file
        folder = save_folder
        if file == "user_list":
            file = "user"
            folder = ""

        file_io.write_csv(folder, f"{file}.csv", GAME_STATE[key])
    
    return "success"
    


if __name__ == "__main__":
    print("test")
