import dearpygui.dearpygui as dpg
import os

# pkg_dir = os.path.dirname(os.path.abspath(__file__))
# font = os.path.join(pkg_dir, "../resources/font/simplto2.ttf")
font = "simplto2.ttf"
dpg.create_context()

# add a font registry
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font(font, 20)
    second_font = dpg.add_font(font, 10)

with dpg.window(label="Font Example", height=200, width=200):
    dpg.add_button(label="Default font")
    dpg.add_button(label="Secondary font", id="Button")
    dpg.add_button(label="default")

    # set font of specific widget
    dpg.bind_font(default_font)
    dpg.bind_item_font("Button", second_font)

dpg.show_font_manager()

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()