class Calculator:
    @staticmethod
    def get_area(length, width):
        return length * width

    @staticmethod
    def get_perimeter(length, width):
        return 2 * (length + width)

    @staticmethod
    def get_volume(length, width, height):
        return length * width * height
