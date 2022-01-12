import configs
import json
from datetime import date

try:
    from win10toast import ToastNotifier
except ImportError:
    print(configs.TOAST_ERROR_MSG)

class Tools:
    @staticmethod
    # renders an image to be displayed on the dearpygui
    def add_and_load_image(dpg, image_path, parent=None):
        width, height, channels, data = dpg.load_image(image_path)

        with dpg.texture_registry() as reg_id:
            texture_id = dpg.add_static_texture(width, height, data, parent=reg_id)

        if parent is None:
            return dpg.add_image(texture_id)
        else:
            return dpg.add_image(texture_id, parent=parent)

    @staticmethod
    # creates the user_data.json file with default configurations
    def create_default_user_data():
        data = {configs.USERDATA_FOCUS_MINS: 15, configs.USERDATA_SMALLBREAK_MINS: 2,
                configs.USERDATA_LONGBREAK_MINS: 25, configs.USERDATA_DATE: {}, configs.USERDATA_TOTAL_FOCUS_MINS: 0,
                configs.USERDATA_TOTAL_POMODOROS: 0}

        # add today's date
        current_date = f"{date.today().month}/{date.today().day}/{date.today().year}"
        data[configs.USERDATA_DATE][current_date] = 0

        Tools.update_user_data(data)

    @staticmethod
    # updates the json file
    def update_user_data(new_data):
        with open(configs.USERDATA_FILEPATH, 'w') as json_file:
            json.dump(new_data, json_file)

    @staticmethod
    def get_current_day():
        current_date = f"{date.today().month}/{date.today().day}/{date.today().year}"
        return current_date

    @staticmethod
    # generates the list of mins that user can choose from
    def create_time_list():
        time_list = []

        # user has the option to choose between 1 min to 60 mins
        for i in range(1, 61):
            time_list.append(i)

        return time_list

    @staticmethod
    def display_notif(title, message, dur):
        toast = ToastNotifier()

        # display toast notification showing that timer is done (win 10 only)
        try:
            toast.show_toast(title, message, duration=dur)
        except:
            print(configs.TOAST_ERROR_MSG)
