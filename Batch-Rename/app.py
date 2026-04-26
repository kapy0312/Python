import os

# 要替換掉的字串清單
REMOVE_STRINGS = [
    "m3u8下载",
    " -加勒逼A片下载",
    " EDmosaic",
    # 之後想加更多，在這裡新增就好
]

def clean_filenames(folder_path):
    folder_path = folder_path.strip().strip('"')  # 去除引號和空白
    
    if not os.path.exists(folder_path):
        print(f"❌ 找不到資料夾：{folder_path}")
        return

    renamed = 0
    skipped = 0

    for filename in os.listdir(folder_path):
        new_name = filename
        
        for s in REMOVE_STRINGS:
            new_name = new_name.replace(s, "")
        
        if new_name != filename:
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"✅ {filename}")
            print(f"   → {new_name}")
            renamed += 1
        else:
            skipped += 1

    print(f"\n完成！共更名 {renamed} 個檔案，{skipped} 個不需更名。")

if __name__ == "__main__":
    folder = input("請輸入資料夾路徑：").strip()
    clean_filenames(folder)