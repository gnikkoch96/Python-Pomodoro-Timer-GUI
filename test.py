import dearpygui.dearpygui as dpg
import dearpygui.logger as dpg_logger

def save_callback():
    print('Save Clicked')


def demo():
    dpg.stop_dearpygui()

    with dpg.window(label='Example Window'):
        dpg.add_text('Hello World')
        dpg.add_button(label='Save', callback=save_callback)  # we applied an onClickListener
        dpg.add_input_text(label='string')  # can input text
        dpg.add_slider_float(label='float')  # slider that allows a float to be chosen

    dpg.setup_viewport()
    dpg.start_dearpygui()


def input_test():
    dpg.stop_dearpygui()

    with dpg.window(label="Input Testing", width=300) as container_one:
        dpg.add_input_text(label="Input One")
        dpg.add_input_text(label="Input Two", default_value="Enter Password")
        dpg.add_slider_float(label="Slider One")
        dpg.add_slider_float(label="Slider Two", default_value=30)

    dpg.setup_viewport()
    dpg.set_viewport_height(100)
    dpg.set_viewport_width(500)
    dpg.start_dearpygui()


def dynamic_change():
    dpg.stop_dearpygui()

    with dpg.window(label="Changing values dynamically", width=300):
        slider_float1 = dpg.add_slider_float(label="Slider One", default_value=15.5, id="slider_one")
        dpg.set_value("slider_one", 100)

    dpg.setup_viewport()
    dpg.set_viewport_width(500)
    dpg.set_viewport_height(100)
    dpg.start_dearpygui()


def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def callback_demo():
    with dpg.window(label="Callback Demo", width=300):
        button = dpg.add_button(label="Callback", callback=button_callback, user_data="some data")

    dpg.setup_viewport()
    dpg.set_viewport_title("Callback Demo")
    dpg.set_viewport_height(100)
    dpg.set_viewport_width(400)
    dpg.start_dearpygui()


logger = dpg_logger.mvLogger()
logger.log("This is my logger. Just like an onion it has many levels.")

def log_things(sender, app_data, user_data):
    user_data.log("We can log to a trace level.")
    user_data.log_debug("We can log to a debug level.")
    user_data.log_info("We can log to an info level.")
    user_data.log_warning("We can log to a warning level.")
    user_data.log_error("We can log to a error level.")
    user_data.log_critical("We can log to a critical level.")


def set_level(sender, app_data, user_data):
    # changing the logger level will ignore any log messages below the set level
    logger = user_data[0]
    level_options = user_data[1]
    logger.log_level = (level_options[dpg.get_value(sender)])

    # we do this so we can see the set level effect
    log_things(sender, app_data, logger)


def logging():
    with dpg.window():
        dpg.add_button(label="Log to logger", callback=log_things, user_data=logger)
        level_options = {"Trace": 0, "Debug": 1, "Info": 2, "Warning": 3, "Error": 4, "Critical": 5}
        dpg.add_radio_button(list(level_options.keys()), callback=set_level, user_data=[logger, level_options])

    dpg.start_dearpygui()


if __name__ == '__main__':
    # demo()
    # input_test()
    # dynamic_change()
    # callback_demo()
    logging()