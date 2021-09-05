import dearpygui.dearpygui as dpg

# main

# n: we get access to the window with the variable name container_one
with dpg.window(label='Container #1') as container_one:
    # container_one will only hold what is inside this function

    button1 = dpg.add_button(label='Press Me')
    slider_int = dpg.add_slider_int(label='Slide to the left', width=100)
    dpg.add_same_line(spacing=10) # adds the slider_int and slider_float to the same line
    slider_float = dpg.add_slider_float(label='Slide to the right!', width=100)

    # to get the id of a component, you have to print them out
    # n: so this means that their id is their .toString()
    print(f"Printing item id's: {container_one}, {button1}, {slider_int}, {slider_float}")

button2 = dpg.add_button(label="Don't forget me!", parent=container_one)
dpg.start_dearpygui()