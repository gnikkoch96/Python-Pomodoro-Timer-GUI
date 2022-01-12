import threading
import time
import dearpygui.dearpygui as dpg

VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000

pic = "resources/images/1.png"

width, height, channels, texture_data = dpg.load_image(pic)
print(dpg.load_image(pic))
dpg.create_context()
dpg.create_viewport(title="(DearPyGUI) Pomodoro Timer", width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
dpg.setup_dearpygui()
dpg.set_global_font_scale(1.25)

with dpg.window(height=VIEWPORT_HEIGHT,
                width=VIEWPORT_WIDTH):
    pass

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

def update_image():
    while (True):
        time.sleep(1)
        width, height, channels, texture_data = dpg.load_image(pic2)
        dpg.set_value("texture_id", texture_data)
        time.sleep(1)
        width, height, channels, texture_data = dpg.load_image(pic1)
        dpg.set_value("texture_id", texture_data)

threading.Thread(target=update_image, daemon=True).start()

