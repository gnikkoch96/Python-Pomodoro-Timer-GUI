import dearpygui.dearpygui as dpg
import os

pkg_path = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(pkg_path, "../resources/images/tomato-banner.png")
print(file)

width, height, channels, data = dpg.load_image(file)

with dpg.texture_registry():
    dpg.add_static_texture(width, height, data, id="texture_id")

with dpg.window(label="Tutorial"):
    dpg.add_image("texture_id")

dpg.start_dearpygui()