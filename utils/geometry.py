class Geometry:

    def calculateCenter(root,window_width,window_height):
        # Calculate the center position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        return '%dx%d+%d+%d' % (window_width, window_height, x_position, y_position)

