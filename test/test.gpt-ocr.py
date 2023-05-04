import os
import keyboard
import requests
import json
from PIL import ImageGrab, Image
import pytesseract
import tkinter as tk
import time
import threading

api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
api_key = "<your_api_key>"

# 在环境变量中查询tesserace可执行程序
tesseract_path = "<your_tesseract_path>\tesseract.exe"
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

    print(f"正在进行OCR识别，请稍等...")
    text = pytesseract.image_to_string(Image.open(save_path))

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": text,
        "max_tokens": 60,
        "temperature": 0.7
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = json.loads(response.text)
        print(result["choices"][0]["text"])
        os.system(f"echo '{result['choices'][0]['text']}'")  # 识别结果展示到命令行???任然输出失败，该行可删除
    else:
        print("Error occurred:", response.text)


keyboard.add_hotkey('ctrl+alt+s', handle_screenshot)
keyboard.add_hotkey('shift+alt+s', handle_screenshot)

class PauseSemaphore:
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()


pause_sem = PauseSemaphore()
ctrl_c_used = False  # 用于判断用户是否已经使用了 Ctrl+C 快捷键


def pause_program():
    global ctrl_c_used
    print("程序已暂停 [ C ] - 继续 [ Q ] - 退出")
    while True:
        key = keyboard.read_event()
        if key.event_type == "down":
            if key.name.lower() == "c":
                print("继续程序")
                break
            elif key.name.lower() == "q":
                print("退出程序")
                exit(0)
            elif key.name.lower() == "ctrl" and not ctrl_c_used:  # 判断是否已经使用过 Ctrl+C
                ctrl_c_used = True
                print("暂停程序")
                pause_sem.acquire()
                break
    events = keyboard.record(until='esc')  # 用 'esc' 作为结束记录的标记
    for event in events:
        pass
    pause_sem.release()


while True:
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        pause_sem.acquire()
        pause_program()
        ctrl_c_used = False  # 重置标记
    except Exception as e:
        print(f"程序暂停: {e}")
        while True:
            try:
                keyboard.wait()
            except KeyboardInterrupt:
                exit(0)
            except:
                time.sleep(3)
                continue
            else:
                break
        pause_sem.acquire()
        pause_program()
        ctrl_c_used = False  # 重置标记
    finally:
        pause_sem.release()

print("程序已退出")
