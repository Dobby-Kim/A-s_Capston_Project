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
    #67: "cell phone",
    73: "book"
}
label_list = list(label_map.keys())

""" 
[x, y, width, height, direction of chair]
direction = 1:Up, 2:Right, 3:Down, 4:Left 
"""
desks = {
    'parksangjo' :[
        [-12, 262, 44, 53, 2],
        [-12, 209, 44, 52, 2],
        [-12, 156, 44, 52, 2],
        [-12, 103, 44, 52, 2],
        [-12, 49, 44, 53, 2],
        [68, -14, 68, 47, 3],
        [137, -14, 52, 47, 3],
        [190, -14, 52, 47, 3],
        [243, -14, 52, 47, 3],
        [296, -14, 90, 47, 3],
        [112, 174, 50, 50, 3],
        [112, 123, 50, 50, 1],
        [163, 174, 53, 50, 3],
        [163, 123, 53, 50, 1],
        [217, 174, 67, 50, 3],
        [217, 123, 67, 50, 1],
        [285, 174, 60, 50, 3],
        [285, 123, 60, 50, 1]
    ],
    'ebstudyroom1' : [
        [0, 6, 150, 92, 4],
        [150, 5, 215, 92, 2],
        [0, 98, 150, 103, 4],
        [150, 97, 215, 103, 2],
        [0, 201, 150, 86, 4],
        [150, 200, 215, 86, 2],
        [0, 287, 150, 115, 4],
        [150, 286, 215, 115, 2]
    ],
    'haedong':[
        [0, 43, 138, 258, 1],
        [145, 43, 300, 258, 1],
        [456, 43, 301, 258, 1],
        [767, 43, 209, 258, 1],
        [148, 337, 122, 136, 1],
        [270, 337, 125, 136, 1],
        [396, 337, 135, 136, 1],
        [530, 337, 125, 136, 1],
        [655, 337, 122, 136, 1],
        [777, 337, 114, 136, 1],
        [148, 474, 122, 187, 3],
        [271, 474, 125, 177, 3],
        [397, 474, 135, 176, 3],
        [533, 474, 125, 176, 3],
        [659, 474, 122, 176, 3],
        [782, 474, 114, 179, 3]
    ]

}
#Park Sang Jo Lounge
H1 = np.array([[5.60419376e-01, 9.71581689e-01, -3.79450113e+02],
            [-3.39450669e-02, 1.77097300e+00, -2.56173657e+02],
            [-1.75642895e-04, 4.53427216e-03, 1.00000000e+00]])
#Engineering Building Studyroom
H2 = np.array([[ 1.37377152e+00,  2.34678778e+00, -1.46687226e+03],
            [-3.12568851e-01,  2.52954456e+00, -4.11804536e+01],
            [ 9.80578801e-04,  3.61712956e-03,  1.00000000e+00]])
#Hae Dong Library
H3 = np.array([[ 2.83839711e+00,  1.60482551e+00, -8.74082214e+02],
            [ 6.33180983e-01,  9.25857095e+00, -4.27796845e+03],
            [-7.09521713e-04,  8.18697677e-03,  1.00000000e+00]])

mtrxs = {
    'parksangjo' : H1,
    'ebstudyroom1': H2,
    'haedong' : H3 
}

def main(space_name,image,original_data,dst_image_name):
    
    # init settings
    
    
    

    ###################################################################################################

    # 1)settings for computation
    # homogeneous matrix for each space; for view transformation
    H = mtrxs[space_name]
    # desk grid setting
    desk = desks[space_name]

    dst_image_path = './img/'+ dst_image_name +'.png'
    original_labels = [item[0] for item in original_data]
    src = image
    dst = cv2.imread(dst_image_path, -1)

    src_shape = (src.shape[1], src.shape[0]) # fixed
    dst_shape = (dst.shape[1] , dst.shape[0])


    # 2) coordiates transformation

    original_coordinates = np.array([[item[1], item[2]] for item in original_data])
    transformed_coordinates = coordinate_transform.transform_coordinates_normalized(original_coordinates, H, src_shape, dst_shape)

    # 3) seat division by hard coded grid
    divided = seat_division.process_seat_division(desk)

    # 4) compute seat occupation
    space_init = seat_occupation.init_space(len(desk))
    detected_pixel = seat_occupation.prop_to_pixel(transformed_coordinates, dst_shape[0], dst_shape[1])
    occupation_final = seat_occupation.seat_occupation(divided, detected_pixel, original_labels, space_init)

    # 5-0) this is for only debuging process: not in the data processing logic
    seat_occupation.display_seat_OpenCV(dst_image_path, divided, detected_pixel, occupation_final)

    
    # 5) update database due to the occupation result
    # 아래의 send_query_to_database 함수는 database에 등록된 컴퓨터의 ip에서만 돌아감.
    updateDatabase.send_query_to_database(space_name, occupation_final) #updated at 23.11.21 by DoYeop
    print(seat_jsonify.list_db_js(space_name, occupation_final))
    print(detected_pixel)
    


# generate temperary img file to be used for yolo model
def run_temp_detect(spaceName, image, opt, dst_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img_file:
        cv2.imwrite(temp_img_file.name, image)
    
    opt.source = temp_img_file.name
    original_data = detection.process_detection(opt)

    
    
    main(spaceName, image, original_data, dst_path)
    
    os.unlink(temp_img_file.name)


if __name__ == "__main__":
    space1 = "parksangjo"
    video_path1 = "./img/"+ space1 +".mp4"
    # Streaming Video Path: 
    video_path1 = "rtsp://admin:ehduq214@172.20.10.4:554/stream1"
    space2 = "ebstudyroom1"
    video_path2 = "./img/"+ space2 +".mp4"
    
    space3 = "haedong"
    video_path3 = "./img/"+ space3 +".mp4"
    
    frame_interval = 20 # ex) if video's frame rate = 20fps and frame_interval = 20 then get frame per 1 sec
    
    default_opts = parse_opt()  # detection.py 의 parse_opt() 가져와 custom_opts 값으로 update
    custom_opts = {'weights': 'yolov5x.pt', 'source': video_path1, 'classes': label_list}
    combined_opts = vars(default_opts)
    combined_opts.update(custom_opts)
    opt = Namespace(**combined_opts)
    
    vidcap1 = cv2.VideoCapture(video_path1)
    #vidcap2 = cv2.VideoCapture(video_path2)
    vidcap3 = cv2.VideoCapture(video_path3)
    
    count = 0

    while True:
        
        success1, image1 = vidcap1.read()
     #   success2, image2 = vidcap2.read()
        success3, image3 = vidcap3.read()
        
        count += 1
    
        if not success1:
            break
        
        if count % frame_interval == 0:
            
            run_temp_detect(space1, image1, opt, space1)
      #      run_temp_detect(space2, image2, opt, space2)
            run_temp_detect(space3, image3, opt, space3)
            
            cv2.imshow('image1', cv2.resize(image1, (1280, 760)))
       #     cv2.imshow('image2', cv2.resize(image2, (1280, 760)))
            cv2.imshow('image3', cv2.resize(image3, (1280, 760)))
            
            if cv2.waitKey(20) == 27:
                break
            
    vidcap1.release()
    vidcap2.release()
    vidcap3.release()
    
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
