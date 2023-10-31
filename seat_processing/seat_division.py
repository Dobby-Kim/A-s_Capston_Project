import cv2

# Tried struct but just ignore it for now
'''class Seat():
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction                          # 1-up 2-right 3-down 4-left'''


# OVERALL LOGIC
# Set seat information by desk only [x, y, width, height, direction]
# direction (of chair) = 1:Up, 2:Right, 3:Down, 4:Left
# x, y is the top-left point of the desk
# Set chair area (pixel) -> chair_area_tl(space_pixel, space_chair)                                     /// space_pixel is space defined by actual pixel
# If needed switch to proportional -> pixel_to_prop(space_pixel, width of image, height of image)
# If needed get centered points -> seat_center(space)                                                   /// space = list of seats
# If in need display by OpenCV -> display_seat_OpenCV(image_path, space)                                /// space = list of seats


# Add chair area in each seat
def chair_area_tl(space_pixel, space_chair):
    space_finalize = []
    for desk in space_pixel:
        x1, y1, x2, y2 = 0, 0, 0, 0
        if desk[4] == 1:
            x1, x2 = desk[0], desk[0]+desk[2]
            y1, y2 = desk[1]-space_chair, desk[1]+desk[3]
        elif desk[4] == 2:
            x1, x2 = desk[0], desk[0]+desk[2]+space_chair
            y1, y2 = desk[1], desk[1]+desk[3]
        elif desk[4] == 3:
            x1, x2 = desk[0], desk[0]+desk[2]
            y1, y2 = desk[1], desk[1]+desk[3]+space_chair
        elif desk[4] == 4:
            x1, x2 = desk[0]-space_chair, desk[0]+desk[2]
            y1, y2 = desk[1], desk[1]+desk[3]
        space_finalize.append([x1, y1, x2, y2])
    return space_finalize


# Turn pixel info into proportional between 0~1 depending on the blueprint
def pixel_to_prop(space_pixel, width, height):
    space_prop = []
    for i in space_pixel:
        space_prop.append([(i[0]/width), (i[1]/height), (i[2]/width), (i[3]/height)])
    return space_prop


# Get center coordinates of seats
def seat_center(space):
    center_coordinates = []
    for i in space:
        center_coordinates.append([(i[0]+i[2])/2, (i[1]+i[3])/2])
    return center_coordinates


# Just to show the seat division in OpenCV
def display_seat_OpenCV(image_path, space):
    blueprint = cv2.imread(image_path)
    for seat in space:
        cv2.rectangle(blueprint, (seat[0], seat[1]), (seat[2], seat[3]), (0, 0, 255), 1)

    #print(seat_center(space))
    cv2.imshow('Seat', blueprint)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0


### SETTING UP DATA (HARD-CODING) ###

# Load image
src_image_path = './img/largeCoordinate.png' 
dst_image_path = './img/roomMap.png'
dst = cv2.imread(dst_image_path, -1)
y_MAX, x_MAX, _ = dst.shape


# [x, y, width, height, direction of chair]
# direction = 1:Up, 2:Right, 3:Down, 4:Left
psj_lounge_desk = [
    [12, 262, 32, 53, 2],
    [12, 209, 32, 52, 2],
    [12, 156, 32, 52, 2],
    [12, 103, 32, 52, 2],
    [12, 49, 32, 53, 2],
    [68, 14, 68, 33, 3],
    [137, 14, 52, 33, 3],
    [190, 14, 52, 33, 3],
    [243, 14, 52, 33, 3],
    [296, 14, 52, 33, 3],
    [112, 174, 50, 50, 3],
    [112, 123, 50, 50, 1],
    [163, 174, 53, 50, 3],
    [163, 123, 53, 50, 1],
    [217, 174, 52, 50, 3],
    [217, 123, 52, 50, 1],
    [270, 174, 60, 50, 3],
    [270, 123, 60, 50, 1]
]


# Collection of space to find with name
space_dict = {}

psj_lounge_with_chair = chair_area_tl(psj_lounge_desk, 15)
psj_lounge_prop = pixel_to_prop(psj_lounge_with_chair, x_MAX, y_MAX)
space_dict["psj"] = psj_lounge_prop
display_seat_OpenCV(dst_image_path, psj_lounge_with_chair)
print(psj_lounge_prop)
#print(psj_lounge_with_chair)