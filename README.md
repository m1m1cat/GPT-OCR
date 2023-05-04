# OpenAI GPT-OCR
[English][url-docen]

这个脚本使用 OpenAI GPT 模型和 Tesseract OCR 引擎实现文字识别。它通过监听键盘快捷键触发截屏操作-用户自选区域裁剪，然后自动识别选区中的文字并将其输入到 GPT 模型中，从而生成文本回复。

本程序只保证你能快捷的利用GPT找到OCR内容结果，Tesseract OCR引擎识别准确度学习需要您自行训练！！！

# 用法
1.首先需要安装以下python模块
* keyboard
* requests
* json
* PIL
* pytesseract
* tkinter
您可以使用命令：
``` 
pip install keyboard requests json pillow pytesseract tkinter
``` 

2.您需要在OpenAI中创建API密钥，并修改脚本中的'api_key'。

3.您需要将Tesseract OCR引擎的可执行文件路径添加到系统环境变量，并设置脚本内'tesseract_path'变量来指定路径。

4.运行脚本。脚本将等待您按下 Ctrl + Alt + S 或 Shift + Alt + S 快捷键来触发截屏操作。截图窗口将打开，您可以使用鼠标选择要识别的文本区域。完成后，输入要保存的文件名，然后按 Enter 键开始识别。

5.脚本将自动识别截图中的文本，并将其输入到 GPT 模型中。生成的回复将显示在控制台中。

# 注意事项
请确保您的系统已安装 Tesseract OCR 引擎，并且已将其可执行文件路径添加到系统环境变量中。
请不要过度使用此脚本，以免超出 OpenAI 的 API 使用限制。

# 捐赠支持
 如果这个项目对你有帮助，你可以给作者发烟 [点我](image/thanku.png)

# 参考链接
https://blog.51cto.com/u_15060515/4189941


# 版本控制
[+] 优化语句，修复小bug。  
[+] 增加GPT-3版本api接口。  
[+] 增加指定tesseract_path，防止自动识别找不到。 
[+] 修复keyboard.wait()阻塞主线程BUG。
[+] 修改只能全屏截图问题，让用户可以自行选取识别内容。  

推荐使用：gpt-ocr.py
测试版本：test-gpt-ocr.py 增加程序暂停功能，ctrl+c不再是直接结束程序，而是暂停程序等待用户选择。存在二次使用快捷键报错BUG


[url-docen]: README_EN.md
