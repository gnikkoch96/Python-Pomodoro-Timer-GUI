import dearpygui.dearpygui as dpg

with dpg.window(label="Delete Files", modal=True, show=False, id="modal_id"):
    dpg.add_text("All those beautiful files will be deleted.\nThis operation cannot be undone!")
    dpg.add_separator()
    dpg.add_checkbox(label="Don't ask me next time")
    dpg.add_button(label="OK", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))
    dpg.add_same_line()
    dpg.add_button(label="Cancel", width=75, callback=lambda: dpg.configure_item("modal_id", show=False))

with dpg.window(label="Tutorial"):

    dpg.add_button(label="Open Dialog", callback=lambda:dpg.configure_item("modal_id", show=True))

dpg.start_dearpygui()