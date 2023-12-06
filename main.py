from util import coordinate_transform
from yolov5 import detection
from util import seat_division
from util import seat_jsonify
from util import seat_occupation
from util import updateDatabase
from util import seat_jsonify

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import tempfile

from argparse import Namespace
from yolov5.detection import parse_opt


# label
label_map = {
    0: "person",
    24: "backpack",
    26: "handbag",
    62: "tv",
    63: "laptop",
    64: "mouse",
    65: "remote",
    66: "keyboard",
    67: "cell phone",
    73: "book"
}
label_list = list(label_map.keys())


def main(original_data):
    # matrix
    H = np.array([[5.60419376e-01, 9.71581689e-01, -3.79450113e+02],
        [-3.39450669e-02, 1.77097300e+00, -2.56173657e+02],
        [-1.75642895e-04, 4.53427216e-03, 1.00000000e+00]])
    
    space_name = "parksangjo"
    
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

    src_image_path = './yolov5/img/psj.jpeg' 
    dst_image_path = './img/roomMap.png'

    ###################################################################################################

    # setting for detection
    '''default_opts = parse_opt() # detection.py 의 parse_opt() 가져와 custom_opts 값으로 update
    custom_opts = {'weights': 'yolov5x.pt', 'source': '0', 'classes': label_list}
    combined_opts = vars(default_opts)
    combined_opts.update(custom_opts)
    opt = argparse.Namespace(**combined_opts)'''


    # 1) detection
    #original_data = detection.process_detection(opt)

    original_labels = [item[0] for item in original_data]

    
    # 2) coordiates transformation
    #src = cv2.imread(src_image_path, -1)
    dst = cv2.imread(dst_image_path, -1)

    src_shape = (1920, 1080) # fixed
    dst_shape = (dst.shape[1] , dst.shape[0])

    original_coordinates = np.array([[item[1], item[2]] for item in original_data])
    transformed_coordinates = coordinate_transform.transform_coordinates_normalized(original_coordinates, H, src_shape, dst_shape)


    # 3) seat division
    divided = seat_division.process_seat_division(psj_lounge_desk)

    
    # 4) seat occupation
    space_init = seat_occupation.init_space(18)
    detected_pixel = seat_occupation.prop_to_pixel(transformed_coordinates, dst.shape[1], dst.shape[0])
    occupation_final = seat_occupation.seat_occupation(divided, detected_pixel, original_labels, space_init)

    #seat_occupation.display_seat_OpenCV(dst_image_path, divided, detected_pixel, occupation_final)
    coordinate_transform.display_transformed_coordinates_matplotlib(
                dst_image_path, detected_pixel, original_labels, label_map, dst_shape
            )
    # 5) jsonify
    # 아래의 함수는 database에 등록된 컴퓨터의 ip에서만 돌아감.
    updateDatabase.send_query_to_database(space_name, occupation_final) #updated at 23.11.21 by DoYeop
    print(seat_jsonify.list_db_js(space_name, occupation_final))
    
    # return detected_pixel, original_labels, dst_shape


if __name__ == "__main__":
    video_path = "./img/sangjotest.mp4"
    frame_interval = 60

    default_opts = parse_opt()  # detection.py 의 parse_opt() 가져와 custom_opts 값으로 update
    custom_opts = {'weights': 'yolov5x.pt', 'source': video_path, 'classes': label_list}
    combined_opts = vars(default_opts)
    combined_opts.update(custom_opts)
    opt = Namespace(**combined_opts)

    #original_data = detection.process_detection(opt)
    #main(original_data)
    
    vidcap = cv2.VideoCapture(video_path)
    count = 0

        
    while True:
        
        success, image = vidcap.read()
        count += 1
        
        if not success:
            break
        
        if count % frame_interval == 0:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img_file:
                cv2.imwrite(temp_img_file.name, image)
        
            opt.source = temp_img_file.name
            original_data = detection.process_detection(opt)
            # detected_pixel, original_labels, dst_shape
            main(original_data)
            
            cv2.imshow('image', image)
            os.unlink(temp_img_file.name)
        

    vidcap.release()
    cv2.destroyAllWindows()
    '''while True:
        start_time = time.time()
        main()
        end_time = time.time()
        elapsed_time = end_time - start_time
        time.sleep(max(8 - elapsed_time, 0)) # 8초마다 반복

        count += 1 # 전체 반복 횟수
        print(count)
    '''
