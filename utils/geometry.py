class Geometry:

    def calculateCenter(root,window_width,window_height):
        # Calculate the center position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        geometry_string = f"{window_width}x{window_height}+{x_position}+{y_position}"

        return geometry_string

