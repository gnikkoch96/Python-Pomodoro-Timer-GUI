import dearpygui.dearpygui as dpg

# add a font registry
with dpg.font_registry():
    # add font (set as default for entire app)
    dpg.add_font("../resources/fonts/simplto2.ttf", 50, default_font=True)

    # add second font
    dpg.add_font("../resources/fonts/Simpleton-Gothic.ttf", 50, id="secondary_font")

with dpg.window(label="Font Example"):
    dpg.add_button(label="Default font")
    dpg.add_button(label="Secondary font")

    # set font of specific widget
    dpg.set_item_font(dpg.last_item(), "secondary_font")

dpg.start_dearpygui()