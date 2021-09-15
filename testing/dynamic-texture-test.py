import dearpygui.dearpygui as dpg
import os
import threading
import time



pkg_dir = os.path.dirname(os.path.abspath(__file__))
pic1 = os.path.join(pkg_dir, "../resources/images/relaxing.gif")
pic2 = os.path.join(pkg_dir, "../resources/images/relaxing - Copy.gif")

width, height, channels, texture_data = dpg.load_image(pic1)

with dpg.texture_registry():
    dpg.add_dynamic_texture(width, height, texture_data, id="texture_id")


with dpg.window(label="Tutorial"):
    dpg.add_image("texture_id")

def update_image():
    while(True):
        time.sleep(1)
        print("hello")
        width, height, channels, texture_data = dpg.load_image(pic2)
        dpg.set_value("texture_id", texture_data)
        time.sleep(1)
        width, height, channels, texture_data = dpg.load_image(pic1)
        dpg.set_value("texture_id", texture_data)

threading.Thread(target=update_image, daemon=True).start()
dpg.start_dearpygui()