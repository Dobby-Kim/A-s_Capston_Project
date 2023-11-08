import cv2

# Initialize empty seats
def init_space(n):
    occupation = []
    for i in range(n):
        occupation.append(0)
    return occupation


# Change detected points from proportional (0~1) to actual pixels
# Width, Height: Blueprint size
def prop_to_pixel(points, width, height):
    points_prop = []
    for point in points:
        points_prop.append([point[0]*width*0.95, point[1]*height*0.85])

    return points_prop


# Check if seat is occupied
# 0: Empty, 1: Reserved (Only objects), 2: Occupied
def seat_occupation(space, points, labels, occupation):
    occupation_final = occupation
    for i in range(len(space)):
        flag = 0
        for p in range(len(points)):
            if space[i][0] <= points[p][0] and points[p][0] <= space[i][2] and space[i][1] <= points[p][1] and points[p][1] <= space[i][3]:
                if labels[p] == 0:
                    occupation_final[i] = 2
                    flag = 2
                elif flag != 2:
                    occupation_final[i] = 1
                    flag = 1
            elif flag == 0:
                occupation_final[i] = 0
    return occupation_final


# Display the division of seats with objects detected
# Empty: Green, Reserved: Orange, Occupied: Red
def display_seat_OpenCV(image_path, space, points, occupation):
    blueprint = cv2.imread(image_path)
    for s in range(len(space)):
        if occupation[s] == 2:
            cv2.rectangle(blueprint, (space[s][0], space[s][1]), (space[s][2], space[s][3]), (0, 0, 255), 1)
        elif occupation[s] == 1:
            cv2.rectangle(blueprint, (space[s][0], space[s][1]), (space[s][2], space[s][3]), (0, 127, 255), 1)
        else:
            cv2.rectangle(blueprint, (space[s][0], space[s][1]), (space[s][2], space[s][3]), (0, 255, 0), 1)
    for point in points:
        cv2.circle(blueprint, (int(point[0]), int(point[1])), 2, (0, 0, 255), -1)
    
    cv2.namedWindow("Seats", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Seats", 640, 480)
    cv2.imshow('Seats', blueprint)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0


# Load image
src_image_path = './img/largeCoordinate.png' 
dst_image_path = './img/roomMap.png'
dst = cv2.imread(dst_image_path, -1)
y_MAX, x_MAX, _ = dst.shape

# Data from coordinate_transform.py for testing
label_map = {
    0: "person",
    73: "book",
    63: "laptop",
    62: "tv",
    65: "remote",
    67: "cell phone",
    64: "mouse",
    66: "keyboard",
    24: "backpack",
    26: "handbag"
}

original_data = [
    [24, 0.05539143458008766, 0.5086705088615417, 0.10960118472576141, 0.2543352544307709],
    [67, 0.8231905698776245, 0.4282711446285248, 0.022156573832035065, 0.0262743029743433],
    [26, 0.1759231835603714, 0.39306357502937317, 0.060561299324035645, 0.14503414928913116],
    [63, 0.6816838979721069, 0.46295323967933655, 0.07415066659450531, 0.05570152401924133],
    [24, 0.7562776803970337, 0.38596951961517334, 0.0762186124920845, 0.06673672795295715],
    [63, 0.5094534754753113, 0.5806621313095093, 0.07769571989774704, 0.10930110514163971],
    [24, 0.7100443243980408, 0.1886495053768158, 0.04697193577885628, 0.07882291078567505],
    [0, 0.7590842247009277, 0.2320021092891693, 0.07474150508642197, 0.20861797034740448],
    [1, 0.4311669170856476, 0.17682605981826782, 0.04224519804120064, 0.05202312022447586]
]
original_labels = [item[0] for item in original_data]

trans_coor = [
    [0.14879968, 0.63583987],
    [0.81870107, 0.55922226],
    [0.18737671, 0.52309312],
    [0.66790606, 0.59618377],
    [0.76936445, 0.50845918],
    [0.511825, 0.69245699],
    [0.83534934, 0.10728809],
    [0.8746065, 0.22739443],
    [0.37910331, 0.0970473]
]

# Data from seat_division.py for testing    /// [x1, y1, x2, y2]
psj = [
    [12, 262, 59, 315],
    [12, 209, 59, 261],
    [12, 156, 59, 208],
    [12, 103, 59, 155],
    [12, 49, 59, 102],
    [68, 14, 136, 62],
    [137, 14, 189, 62],
    [190, 14, 242, 62],
    [243, 14, 295, 62],
    [296, 14, 348, 62],
    [112, 174, 162, 239],
    [112, 108, 162, 173],
    [163, 174, 216, 239],
    [163, 108, 216, 173],
    [217, 174, 269, 239],
    [217, 108, 269, 173],
    [270, 174, 330, 239],
    [270, 108, 330, 173]
]

psj2 = [
    [12, 262, 64, 315],
    [12, 209, 64, 261],
    [12, 156, 64, 208],
    [12, 103, 64, 155],
    [12, 49, 64, 102],
    [68, 14, 136, 67],
    [137, 14, 189, 67],
    [190, 14, 242, 67],
    [243, 14, 295, 67],
    [296, 14, 348, 67],
    [112, 174, 162, 244],
    [112, 103, 162, 173],
    [163, 174, 216, 244],
    [163, 103, 216, 173],
    [217, 174, 269, 244],
    [217, 103, 269, 173],
    [270, 174, 330, 244],
    [270, 103, 330, 173]
]

psj_prop = [
    [0.028985507246376812, 0.8111455108359134, 0.14251207729468598, 0.9752321981424149],
    [0.028985507246376812, 0.6470588235294118, 0.14251207729468598, 0.8080495356037152],
    [0.028985507246376812, 0.48297213622291024, 0.14251207729468598, 0.6439628482972136],
    [0.028985507246376812, 0.3188854489164087, 0.14251207729468598, 0.47987616099071206],
    [0.028985507246376812, 0.15170278637770898, 0.14251207729468598, 0.3157894736842105],
    [0.1642512077294686, 0.043343653250773995, 0.3285024154589372, 0.19195046439628483],
    [0.3309178743961353, 0.043343653250773995, 0.45652173913043476, 0.19195046439628483],
    [0.45893719806763283, 0.043343653250773995, 0.5845410628019324, 0.19195046439628483],
    [0.5869565217391305, 0.043343653250773995, 0.7125603864734299, 0.19195046439628483],
    [0.714975845410628, 0.043343653250773995, 0.8405797101449275, 0.19195046439628483],
    [0.27053140096618356, 0.5386996904024768, 0.391304347826087, 0.739938080495356],
    [0.27053140096618356, 0.33436532507739936, 0.391304347826087, 0.5356037151702786],
    [0.39371980676328505, 0.5386996904024768, 0.5217391304347826, 0.739938080495356],
    [0.39371980676328505, 0.33436532507739936, 0.5217391304347826, 0.5356037151702786],
    [0.5241545893719807, 0.5386996904024768, 0.6497584541062802, 0.739938080495356],
    [0.5241545893719807, 0.33436532507739936, 0.6497584541062802, 0.5356037151702786],
    [0.6521739130434783, 0.5386996904024768, 0.7971014492753623, 0.739938080495356],
    [0.6521739130434783, 0.33436532507739936, 0.7971014492753623, 0.5356037151702786]
]

# Initializing empty occupation (later can call on existing data)
psj_init = init_space(18)

detected_pixel = prop_to_pixel(trans_coor, x_MAX, y_MAX)
#seat_occupation(psj_prop, temp1, original_labels, temp)
#temp2 = seat_occupation(psj_prop, trans_coor, original_labels, temp)
#print(temp2)
psj_final = seat_occupation(psj2, detected_pixel, original_labels, psj_init)
print(psj_final)
display_seat_OpenCV(dst_image_path, psj2, detected_pixel, psj_final)