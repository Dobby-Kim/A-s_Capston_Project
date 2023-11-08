import argparse
import seat_division
import seat_jsonify
import seat_occupation
import coordinate_transform
import detection
import seat_jsonify
import numpy as np
import cv2
import time
from argparse import Namespace
from detection import parse_opt

def main():

    # label
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

    label_list = list(label_map.keys())

    # matrix
    H = np.array([[5.60419376e-01, 9.71581689e-01, -3.79450113e+02],
        [-3.39450669e-02, 1.77097300e+00, -2.56173657e+02],
        [-1.75642895e-04, 4.53427216e-03, 1.00000000e+00]])
    
    space_name = "psj"
    
    # desk
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

    src_image_path = './img/psj.jpeg' 
    dst_image_path = './img/roomMap.png'

    ###################################################################################################

    # setting for detection
    default_opts = parse_opt() # detection.py 의 parse_opt() 가져와 custom_opts 값으로 update
    custom_opts = {'weights': 'yolov5x.pt', 'source': '0', 'classes': label_list}
    combined_opts = vars(default_opts)
    combined_opts.update(custom_opts)
    opt = argparse.Namespace(**combined_opts)


    # 1) detection
    original_data = detection.process_detection(opt)

    original_labels = [item[0] for item in original_data]

    
    # 2) coordiates transformation
    src = cv2.imread(src_image_path, -1)
    dst = cv2.imread(dst_image_path, -1)

    src_shape = (src.shape[0] , src.shape[1])
    dst_shape = (dst.shape[0] , dst.shape[1])

    original_coordinates = np.array([[item[1], item[2]] for item in original_data])
    transformed_coordinates = coordinate_transform.transform_coordinates_normalized(original_coordinates, H, src_shape, dst_shape)


    # 3) seat division
    divided = seat_division.process_seat_division(psj_lounge_desk)

    
    # 4) seat occupation
    space_init = seat_occupation.init_space(18)
    detected_pixel = seat_occupation.prop_to_pixel(transformed_coordinates, dst.shape[1], dst.shape[0])
    occupation_final = seat_occupation.seat_occupation(divided, detected_pixel, original_labels, space_init)


    # 5) jsonify
    print(seat_jsonify.list_db_js(space_name, occupation_final))



if __name__ == "__main__":
    count = 0
    
    while True:
        start_time = time.time()
        main()
        end_time = time.time()
        elapsed_time = end_time - start_time
        time.sleep(max(8 - elapsed_time, 0)) # 8초마다 반복

        count += 1 # 전체 반복 횟수
        print(count) 
        