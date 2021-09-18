# so far we can only add padding and add and load images
class Tools:
    @staticmethod
    def add_padding(dpg, width_value=0, height_value=0, is_same_line=False):
        if height_value != 0:
            dpg.add_dummy(height=height_value)

        if width_value != 0:
            dpg.add_dummy(width=width_value)

        if is_same_line:
            dpg.add_same_line()

    @staticmethod
    def add_and_load_image(dpg, image_path, parent=None):
        width, height, channels, data = dpg.load_image(image_path)

        with dpg.texture_registry() as reg_id:
            texture_id = dpg.add_static_texture(width, height, data, parent=reg_id)

        if parent is None:
            return dpg.add_image(texture_id)
        else:
            return dpg.add_image(texture_id, parent=parent)