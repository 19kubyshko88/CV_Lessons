import time
import numpy as np
from cv2 import cv2

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, -50) # настройка яркости камеры (примерно -150 до 150)

pTime, cTime = 0, 0


# contants
tool_panel_x_pos = 150 # отступ по х для панели инструментов
curr_tool = "select tool"
curr_tool = "line"
time_init = True
rad = 40 # радиус круга, к-рый появляется при наведении на инструмент
var_inits = False
thick = 4
prevx, prevy = 0, 0

# drawing tools
tools = cv2.imread("tools.png")
tools: np.ndarray = tools.astype('uint8')
panel_height, panel_width, _ = tools.shape
max_x, max_y = panel_width + tool_panel_x_pos, panel_height

# get tools function
def getTool(x):
    if x < 50 + tool_panel_x_pos:
        return "line"

    elif x < 100 + tool_panel_x_pos:
        return "rectangle"

    elif x < 150 + tool_panel_x_pos:
        return "draw"

    elif x < 200 + tool_panel_x_pos:
        return "circle"

    else:
        return "erase"


def show_fps(img, show: bool):
    global pTime, cTime
    if show:
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,
                    str(int(fps)),
                    (10, 50),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (255, 0, 255),
                    3)
    return img

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # отзеркаливание изображения

    img[:max_y, tool_panel_x_pos:max_x] = cv2.addWeighted(tools, 1, img[:max_y, tool_panel_x_pos:max_x], 0.3, 0.5)

    img = show_fps(img, True)

    cv2.imshow("Img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'): # Esc = 27
        break