import cv2 as cv
import os
import sys


class TileSectioningSetup:
    def __init__(self, image):
        self.image = image
        self.image_size = {"x": image.shape[1], "y": image.shape[0]}
        self.tile_size = None
        self.target_dir = None

    @property
    def img_size_x(self):
        return self.image_size["x"]

    @property
    def img_size_y(self):
        return self.image_size["y"]

    @property
    def px_total(self):
        return self.img_size_x * self.img_size_y

    @property
    def number_of_tiles_x(self):
        return int(self.image_size["x"] / self.tile_size)

    @property
    def number_of_tiles_y(self):
        return int(self.image_size["y"] / self.tile_size)

    @property
    def lost_px_x(self):
        left, right = self._lost_px(self.img_size_x, self.tile_size)
        return left + right

    @property
    def lost_px_left(self):
        return self._lost_px(self.img_size_x, self.tile_size)[0]

    @property
    def lost_px_right(self):
        return self._lost_px(self.img_size_x, self.tile_size)[1]

    @property
    def lost_px_y(self):
        top, bottom = self._lost_px(self.img_size_y, self.tile_size)
        return top + bottom

    @property
    def lost_px_top(self):
        return self._lost_px(self.img_size_y, self.tile_size)[0]

    @property
    def lost_px_bottom(self):
        return self._lost_px(self.img_size_y, self.tile_size)[1]

    @property
    def lost_px_total(self):
        return self.lost_px_x * self.img_size_y + self.lost_px_y * (self.img_size_x - self.lost_px_x)

    @property
    def lost_px_total_percentage(self):
        return int(100 * self.lost_px_total / self.px_total)

    @staticmethod
    def _lost_px(full_length, section_length):
        lost_px = full_length % section_length
        lost_px_1 = int(lost_px / 2)
        lost_px_2 = lost_px - lost_px_1
        return lost_px_1, lost_px_2

    def cut_lost_px(self):
        x1 = self.lost_px_left
        x2 = self.img_size_x - self.lost_px_right
        y1 = self.lost_px_top
        y2 = self.img_size_y - self.lost_px_bottom
        cropped_image = self.image[y1:y2, x1:x2]
        # cv.imwrite("test.jpg", cropped_image)
        return cropped_image

    def cut_tiles(self):
        self.create_target_dir()
        cropped_image = self.cut_lost_px()
        for y in range(0, self.number_of_tiles_y):
            for x in range(0, self.number_of_tiles_x):
                x1 = x * self.tile_size
                x2 = (x + 1) * self.tile_size
                y1 = y * self.tile_size
                y2 = (y + 1) * self.tile_size
                tile = cropped_image[y1:y2, x1:x2]
                print(f"creating tile {y}/{x}")
                tile_file_path = os.path.join(self.target_dir, f"tile_{y+1}_{x+1}.jpg")
                cv.imwrite(tile_file_path, tile)

    def create_target_dir(self):
        if not os.path.isdir(self.target_dir):
            os.mkdir(self.target_dir)
            print(f"created directory {self.target_dir}")


if __name__ == "__main__":
    image_path = sys.argv[1]
    dir_path, image_name = os.path.split(os.path.abspath(image_path))

    tss = TileSectioningSetup(cv.imread(image_path))

    print(f"imported {image_name}\nwidth={tss.img_size_x}\nheight={tss.img_size_y}")
    user_input = input("Enter your desired tile size: ")
    tss.tile_size = int(user_input)

    print(f"The image will be converted into {tss.number_of_tiles_x}(x) and {tss.number_of_tiles_y}(y) tiles losing "
          f"   \n{tss.lost_px_left} pixels on the left"
          f"   \n{tss.lost_px_right} on the right"
          f"   \n{tss.lost_px_top} on the top"
          f"   \n{tss.lost_px_bottom} on the bottom"
          f"   \nlost pixels in total: {tss.lost_px_total}"
          f"({tss.lost_px_total_percentage}%)")

    # create folder
    tss.target_dir = os.path.join(dir_path, image_name + "_tiles")


    tss.cut_tiles()










