import os
import keyboard
import requests
import json
from PIL import ImageGrab, Image
import pytesseract
import tkinter as tk
import time
import sys


# GPT-api key
# GPT3.5 api_url = "https://api.openai.com/v1/engines/davinci-002/completions"
api_url = "https://api.openai.com/v1/engines/davinci/completions"
api_key = "<your_api_key>"


# 在环境变量中查询tesserace可执行程序
tesseract_path = "<your_path>tesseract.exe"
if os.path.isfile(tesseract_path):
    print(f"找到文件位置： {tesseract_path}")
    print("请按截图键->灰窗出现鼠标左键按住选区！")
    os.environ["PATH"] += os.pathsep + os.path.dirname(tesseract_path)
else:
    print("找不到tesseract.exe")
    exit(1)


class ScreenshotWindow:
    def __init__(self, master):
        self.master = master
        self.master.attributes("-alpha", 0.3)
        self.master.attributes("-fullscreen", True)
        self.master.bind("<ButtonPress-1>", self.on_down)
        self.master.bind("<ButtonRelease-1>", self.on_up)
        self.master.bind("<Escape>", self.cancel)
        self.rect = None

    def on_down(self, event):
        self.rect = [event.x_root, event.y_root, 0, 0]

    def on_up(self, event):
        self.rect[2], self.rect[3] = event.x_root, event.y_root
        self.master.destroy()

    def cancel(self, event):
        self.rect = None
        self.master.destroy()


def handle_screenshot():
    root = tk.Tk()
    app = ScreenshotWindow(root)
    root.mainloop()

    if not app.rect:
        return

    dir_path = os.getcwd()

    print(f"正在截取屏幕区域：{app.rect}")
    im = ImageGrab.grab()
    im_crop = im.crop(app.rect)
    screenshot_path = os.path.join(dir_path, "temp.png")
    im_crop.save(screenshot_path)

    print(f"截图已保存为{os.path.basename(screenshot_path)}，请输入文件名并按Enter键开始识别。")
    filename = input("文件名：")
    if filename.strip() == "":
        filename = "screenshot"
    filename += ".png"
    save_path = os.path.join(dir_path, filename)
    if os.path.isfile(save_path):
        print("文件名已存在，请重新输入文件名。")
        filename = input("文件名：")
        if filename.strip() == "":
            filename = "screenshot"
        filename += ".png"
        save_path = os.path.join(dir_path, filename)
    os.rename(screenshot_path, save_path)

# data参数解析：max_token-返回内容长度，temperature-GPT创造性参数（数值越高回答越多样化，数值低回答文本相似）
    print(f"正在进行OCR识别，请稍等...")
    text = pytesseract.image_to_string(Image.open(save_path))

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": text,
        "max_tokens": 200,
        "temperature": 0.6
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = json.loads(response.text)
        print(result["choices"][0]["text"])
    else:
        print("Error occurred:", response.text)

# 注册快捷键
keyboard.add_hotkey('ctrl+alt+s', handle_screenshot)
keyboard.add_hotkey('shift+alt+s', handle_screenshot)

# 循环程序，5秒睡眠防止系统占用
while True:
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"程序暂停: {e}")
        time.sleep(5)
        continue

print("程序已退出")
sys.exit(0)

