# OpenAI GPT-OCR

This script uses the OpenAI GPT model and Tesseract OCR engine to perform text recognition. It triggers a screenshot operation by listening for keyboard shortcuts - the user selects the region to be cropped, and then automatically recognizes the text in the selected area and inputs it into the GPT model to generate text replies.

This program only guarantees that you can quickly use GPT to find OCR content results, and the accuracy of Tesseract OCR engine recognition needs to be learned and trained by yourself!!!

# Usage
1.First, you need to install the following Python modules
* keyboard
* requests
* json
* PIL
* pytesseract
* tkinter

You can use the command:
``` 
pip install keyboard requests json pillow pytesseract tkinter
``` 
or
``` 
pip install -r requirements.txt
``` 

2.You need to create an API key in OpenAI and modify 'api_key' in the script.

3.You need to add the executable file path of the Tesseract OCR engine to the system environment variables and set the 'tesseract_path' variable in the script to specify the path.

4.Run the script. The script will wait for you to press the Ctrl + Alt + S or Shift + Alt + S keyboard shortcuts to trigger the screenshot operation. The screenshot window will open, and you can use the mouse to select the text area to be recognized. After completion, enter the filename to be saved and press Enter to start recognition.

5.The script will automatically recognize the text in the screenshot and input it into the GPT model. The generated reply will be displayed in the console.

# 注意事项
Please make sure that the Tesseract OCR engine is installed on your system and its executable file path has been added to the system environment variables.
Please do not overuse this script to avoid exceeding the OpenAI API usage limit.

# Demo/Tesseract recognition accuracy



https://user-images.githubusercontent.com/29671030/236109188-9fdcec07-efaf-4f4b-a791-80c365c52d10.mp4

The accuracy of Tesseract recognition may cause problems with the program results and needs to be trained to improve accuracy.


![微信截图_20230504120130](https://user-images.githubusercontent.com/29671030/236110141-30bae4fb-556d-4aa1-ad84-2f815af59ddd.png)



# Donation support
 如果这个项目对你有帮助，你可以给作者发烟 [点我](image/thanku.png)

# Reference links
https://blog.51cto.com/u_15060515/4189941


# Version control
[+] Optimized statements, fixed small bugs.  
[+] Add script loop function and set sleep to prevent excessive system usage.  
[+] Added GPT-3 version API interface.  
[+] Added 'tesseract_path' to prevent automatic recognition from not finding the path.  
[+] Fixed the bug where 'keyboard.wait()' blocked the main thread.  
[+] Modified the problem of only being able to take full-screen screenshots, allowing users to select the recognition content themselves.  

Recommended use: gpt-ocr.py
Test version: test-gpt-ocr.py adds the pause function of the program, and ctrl+c is no longer directly ending the program, but pausing the program to wait for the user to select. There is a bug where the shortcut key is used for the second time.
