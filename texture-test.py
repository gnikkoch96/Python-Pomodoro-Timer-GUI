import dearpygui.dearpygui as dpg

width, height, channels, texture_data = dpg.load_image('resources/images/tomato-banner.png')

with dpg.texture_registry():
    dpg.add_static_texture(width, height, texture_data, id="texture_id")

with dpg.window(label="Tutorial"):
    dpg.add_image("texture_id")

dpg.start_dearpygui()