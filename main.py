import pyautogui
import time
import mss
from PIL import Image, ImageDraw
import pyperclip
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


def detect_and_input_password():

    # 等待弹窗出现

    print("detect_and_input_password")

    box, monitor = detect_the_password_box("box.png")

    password_input = (box.left + 10, box.top + 10)

    print("password_input")
    print(password_input)
    print("monitor")
    print(monitor)

    with mss.mss() as sct:

        monitorScreenshot = sct.grab(monitor)
        img = Image.frombytes(
            "RGB", monitorScreenshot.size, monitorScreenshot.bgra, "raw", "BGRX"
        )

        username_input = (box.left + 500, box.top + 185)
        password_input = (box.left + 500, box.top + 240)
        allow_button = (box.left + 750, box.top + 320)
        # drawStar(img, box.left + 500, box.top + 185)
        # drawStar(img, box.left + 500, box.top + 240)
        # drawStar(img, box.left + 750, box.top + 320)

    pyautogui.moveTo(username_input[0] / 2, username_input[1] / 2, duration=0.1)
    pyautogui.click()
    pyperclip.copy(username)
    pyautogui.hotkey("command", "a")
    pyautogui.hotkey("command", "v")

    pyautogui.moveTo(password_input[0] / 2, password_input[1] / 2, duration=0.1)
    pyperclip.copy(password)
    pyautogui.click()
    pyautogui.hotkey("command", "a")
    pyautogui.hotkey("command", "v")

    pyautogui.moveTo(allow_button[0] / 2, allow_button[1] / 2, duration=0.1)
    pyautogui.click()


def detect_the_password_box(box_path):
    print("detect_the_password_box")

    with mss.mss() as sct:
        # 获取所有显示器的截图
        monitors = sct.monitors[1:]  # 跳过第一个元素，因为它是整个虚拟屏幕

        print("len(sct.monitors)")
        print(len(sct.monitors))

        for i, monitor in enumerate(monitors):
            # 截取每个显示器的内容

            # 在截取的图像中搜索目标

            try:

                box = find_box_in_screen(monitor, box_path)

                if box:
                    print(f"box found on screen {i + 1} at {box}")
                    return box, monitor
            except Exception as e:
                print(str(e))
                print(f"box not found on screen {i + 1}")
        print("Image not found on any screen.")
        return False


def find_box_in_screen(monitor, box_path, confidence=0.5):

    with mss.mss() as sct:

        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        img.save(f"./debug/screenshot-{monitor.__hash__}.png")

        box = pyautogui.locate(
            needleImage=box_path,
            haystackImage=img,
            grayscale=True,
            confidence=confidence,
        )

        draw = ImageDraw.Draw(img)

        # 转换为左上角和右下角坐标
        x0, y0 = box.left, box.top
        x1, y1 = x0 + box.width, y0 + box.height
        draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
        # 保存截图
        img.save("./debug/found_box.png")
        print("Saved debug screenshot with highlighted box")

        return box


def drawStar(image, x, y):

    draw = ImageDraw.Draw(image)

    # 设置十字标记的尺寸
    cross_size = 10  # 控制十字的长度
    color = "red"  # 十字标记颜色

    # 绘制水平线
    draw.line((x - cross_size, y, x + cross_size, y), fill=color, width=2)

    # 绘制垂直线
    draw.line((x, y - cross_size, x, y + cross_size), fill=color, width=2)

    # 保存或显示图像
    image.save("debug_cross_mark.png")
    image.show()


if __name__ == "__main__":
    error_count = 0  # 初始化错误计数器

    while True:
        try:
            # 调用主逻辑
            detect_and_input_password()

            # 逻辑成功后重置错误计数器
            error_count = 0

        except Exception as e:
            # 捕获异常并打印错误信息
            print("An error occurred:", e)

            # 增加错误计数器
            error_count += 1

            # 每次执行后的延迟
            time.sleep(error_count * 0.5)

            # 检查错误计数器是否达到3次
            if error_count >= 3:
                print("Too many errors. Exiting the process.")
                break  # 退出循环
