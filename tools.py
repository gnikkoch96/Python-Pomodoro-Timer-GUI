# so far we can only add padding and add and load images
import configs
import json
from datetime import date


class Tools:
    @staticmethod
    def add_and_load_image(dpg, image_path, parent=None):
        width, height, channels, data = dpg.load_image(image_path)

        with dpg.texture_registry() as reg_id:
            texture_id = dpg.add_static_texture(width, height, data, parent=reg_id)

        if parent is None:
            return dpg.add_image(texture_id)
        else:
            return dpg.add_image(texture_id, parent=parent)

    @staticmethod
    def create_default_user_data():
        data = {configs.USERDATA_FOCUS_MINS: 15, configs.USERDATA_SMALLBREAK_MINS: 2,
                configs.USERDATA_LONGBREAK_MINS: 25, configs.USERDATA_DATE: {}, configs.USERDATA_TOTAL_FOCUS_MINS: 0,
                configs.USERDATA_TOTAL_POMODOROS: 0}

        # add today's date
        current_date = f"{date.today().month}/{date.today().day}/{date.today().year}"
        data[configs.USERDATA_DATE][current_date] = 0

        with open(configs.USERDATA_FILEPATH, 'w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def get_current_day():
        current_date = f"{date.today().month}/{date.today().day}/{date.today().year}"
        return current_date
