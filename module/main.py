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

import psutil
import GPUtil
import time

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
    #seat_occupation.display_seat_OpenCV(dst_image_path, divided, detected_pixel, occupation_final)

    
    # 5) update database due to the occupation result
    # 아래의 send_query_to_database 함수는 database에 등록된 컴퓨터의 ip에서만 돌아감.
    # updateDatabase.send_query_to_database(space_name, occupation_final) #updated at 23.11.21 by DoYeop
    #print(seat_jsonify.list_db_js(space_name, occupation_final))
    #print(detected_pixel)
    


# generate temperary img file to be used for yolo model
def run_temp_detect(spaceName, image, opt, dst_path, exec_time_list1, exec_time_list2):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img_file:
        cv2.imwrite(temp_img_file.name, image)
    
    opt.source = temp_img_file.name
    
    try:
        start_time = time.time()

        original_data = detection.process_detection(opt)
        
        end_time = time.time()
        
        executed_time1 = end_time - start_time
        exec_time_list1.append(executed_time1)
    except:
        pass
        
    
    try:
        start_time = time.time()
        
        main(spaceName, image, original_data, dst_path)
    
        end_time = time.time()
        
        executed_time2 = end_time - start_time
        exec_time_list2.append(executed_time2)
    except:
        pass
    
    #print(f"Every detection time: ", exec_time_list1)  
    print(f"Average detection time: {np.mean(exec_time_list1)} seconds") 
    #print(f"Every Data processing time: ", exec_time_list2)  
    print(f"Average Data processing time: {np.mean(exec_time_list2)} seconds") 
    
    
    os.unlink(temp_img_file.name)
    
    return exec_time_list1, exec_time_list2 



def draw_detection_plot(cycle, time_list, name, num):
    fig = plt.figure()

    ax = fig.add_subplot()
    ax.plot(cycle, time_list, label = 'Execution Time', color='green')
    
    # Calculate and plot the mean of the time_list
    mean_time = np.mean(time_list)
    max_time = np.max(time_list)
    min_time = np.min(time_list)
    
    ax.axhline(mean_time, color='gray', linestyle='--', label=f'Avg: {mean_time:.2f}sec')
    ax.axhline(max_time, color='red', linestyle='--', label=f'Max: {max_time:.2f}sec')
    ax.axhline(min_time, color='blue', linestyle='--', label=f'Min: {min_time:.2f}sec') 

    # Set the y-axis limit to show only between 0 and 1
    # ax.set_ylim(0, 1)

    # plt.yticks(np.linspace(0, 1, 10))  # Set y-ticks to be more descriptive

    plt.title(f'{name} Execution Time')
    plt.xlabel('Cycle')
    plt.ylabel('Execution Time (s)')
    plt.legend()

    plt.savefig(f'{name}_execution_time{num}.png')
    print(f"{name}{num} Graphs saved.")
    
    plt.show()
    
    
def draw_processing_plot(cycle, time_list, name, num):
    
    fig = plt.figure()

    time_list = [1000 * exec_time for exec_time in time_list]
    
    ax = fig.add_subplot()
    ax.plot(cycle, time_list, label = 'Execution Time', color='green')
    
    # Calculate and plot the mean of the time_list
    mean_time = np.mean(time_list)
    max_time = np.max(time_list)
    min_time = np.min(time_list)
    
    ax.axhline(mean_time, color='gray', linestyle='--', label=f'Avg: {mean_time:.2f}ms')
    ax.axhline(max_time, color='red', linestyle='--', label=f'Max: {max_time:.2f}ms')
    ax.axhline(min_time, color='blue', linestyle='--', label=f'Min: {min_time:.2f}ms') 

    # Set the y-axis limit to show only between 0 and 1
    # ax.set_ylim(0, 5)

    # plt.yticks(np.linspace(0, 5, 10))  # Set y-ticks to be more descriptive

    plt.title(f'{name} Execution Time')
    plt.xlabel('Cycle')
    plt.ylabel('Execution Time (ms)')
    plt.legend()

    plt.savefig(f'{name}_execution_time{num}.png')
    print(f"{name}{num} Graphs saved.")
    
    plt.show()


def get_system_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().used / (1024 ** 2)
    gpu_usage = GPUtil.getGPUs()[0].memoryUsed if GPUtil.getGPUs() else 0  # 첫 번째 GPU의 사용량 (퍼센트로 변환)
    return cpu_usage, ram_usage, gpu_usage


def plot_and_save_results(timestamps, cpu_usages, ram_usages, gpu_usages):
    # 시간 변환 (UNIX timestamp to readable format)

    # 플롯 생성
    plt.figure(figsize=(15, 5))

    # CPU 사용량 플롯
    plt.subplot(1, 3, 1)
    plt.plot(timestamps, cpu_usages, label='CPU Usage Change', color='blue')
    plt.xlabel('Cycle')
    plt.ylabel('Usage (%)')
    plt.title('CPU Usage Change Over Cycle')
    plt.xticks(rotation=45)

    # CPU 사용량의 평균, 최대, 최소에 대한 점선 추가
    cpu_avg, cpu_max, cpu_min = np.mean(cpu_usages), np.max(cpu_usages), np.min(cpu_usages)
    plt.axhline(cpu_avg, color='gray', linestyle='--', label=f'Avg: {cpu_avg:.2f}%')
    plt.axhline(cpu_max, color='orange', linestyle='--', label=f'Max: {cpu_max:.2f}%')
    plt.axhline(cpu_min, color='purple', linestyle='--', label=f'Min: {cpu_min:.2f}%')
    plt.legend()

    # RAM 사용량 플롯
    plt.subplot(1, 3, 2)
    plt.plot(timestamps, ram_usages, label='RAM Usage Change', color='red')
    plt.xlabel('Cycle')
    plt.ylabel('Usage (MB)')
    plt.title('RAM Usage Change Over Cycle')
    plt.xticks(rotation=45)

    # RAM 사용량의 평균, 최대, 최소에 대한 점선 추가
    ram_avg, ram_max, ram_min = np.mean(ram_usages), np.max(ram_usages), np.min(ram_usages)
    plt.axhline(ram_avg, color='gray', linestyle='--', label=f'Avg: {ram_avg:.2f} MB')
    plt.axhline(ram_max, color='orange', linestyle='--', label=f'Max: {ram_max:.2f} MB')
    plt.axhline(ram_min, color='purple', linestyle='--', label=f'Min: {ram_min:.2f} MB')
    plt.legend()

    # GPU 사용량 플롯
    plt.subplot(1, 3, 3)
    plt.plot(timestamps, gpu_usages, label='GPU Usage Change', color='green')
    plt.xlabel('Cycle')
    plt.ylabel('Usage (MB)')
    plt.title('GPU Usage Change Over Cycle')
    plt.xticks(rotation=45)

    # GPU 사용량의 평균, 최대, 최소에 대한 점선 추가
    gpu_avg, gpu_max, gpu_min = np.mean(gpu_usages), np.max(gpu_usages), np.min(gpu_usages)
    plt.axhline(gpu_avg, color='gray', linestyle='--', label=f'Avg: {gpu_avg:.2f} MB')
    plt.axhline(gpu_max, color='orange', linestyle='--', label=f'Max: {gpu_max:.2f} MB')
    plt.axhline(gpu_min, color='purple', linestyle='--', label=f'Min: {gpu_min:.2f} MB')
    plt.legend()

    plt.tight_layout()

    # 그래프 이미지 파일로 저장
    plt.savefig('system_usage_graphs_with_stats.png')
    print("Graphs with stats saved to 'system_usage_graphs_with_stats.png'.")

    plt.show()


cpu_usages = []
ram_usages = []
gpu_usages = []
timestamps = []

cpu_usage_before, ram_usage_before, gpu_usage_before = get_system_usage()


if __name__ == "__main__":
    space1 = "parksangjo"
    video_path1 = "./img/"+ space1 +".mp4"
    # Streaming Video Path: 
    # video_path1 = "rtsp://admin:ehduq214@172.20.10.4:554/stream1"
    space2 = "ebstudyroom1"
    video_path2 = "./img/"+ space2 +".mp4"
    
    space3 = "haedong"
    video_path3 = "./img/"+ space3 +".mp4"
    
    frame_interval = 10 # ex) if video's frame rate = 20fps and frame_interval = 20 then get frame per 1 sec
    
    default_opts = parse_opt()  # detection.py 의 parse_opt() 가져와 custom_opts 값으로 update
    custom_opts = {'weights': 'yolov5x.pt', 'source': video_path1, 'classes': label_list}
    combined_opts = vars(default_opts)
    combined_opts.update(custom_opts)
    opt = Namespace(**combined_opts)
    
    vidcap1 = cv2.VideoCapture(video_path1)
    vidcap2 = cv2.VideoCapture(video_path2)
    vidcap3 = cv2.VideoCapture(video_path3)
    
    count = 0
    flag = 0
    detection_time_list1 = []
    data_processing_time_list1 = []
    
    detection_time_list2 = []
    data_processing_time_list2 = []
    
    detection_time_list3 = []
    data_processing_time_list3 = []

    cycle = 0
    while True:
        
        success1, image1 = vidcap1.read()
        success2, image2 = vidcap2.read()
        success3, image3 = vidcap3.read()
        
        count += 1
    
        if not (success1 and success2 and success3):
            break
        
        if count % frame_interval == 0:
            cycle += 1
            
            detection_time_list1, data_processing_time_list1 = run_temp_detect(space1, image1, opt, space1, detection_time_list1, data_processing_time_list1)
            detection_time_list2, data_processing_time_list2 = run_temp_detect(space2, image2, opt, space2, detection_time_list2, data_processing_time_list2)
            detection_time_list3, data_processing_time_list3 = run_temp_detect(space3, image3, opt, space3, detection_time_list3, data_processing_time_list3)
            
            #cv2.imshow('image1', cv2.resize(image1, (1280, 760)))
            #cv2.imshow('image2', cv2.resize(image2, (1280, 760)))
            #cv2.imshow('image3', cv2.resize(image3, (1280, 760)))
            
            if cv2.waitKey(20) == 27:
                break

    #         cpu_usage_after, ram_usage_after, gpu_usage_after = get_system_usage()
    #         cpu_usage_change = cpu_usage_after - cpu_usage_before
    #         ram_usage_change = ram_usage_after - ram_usage_before
    #         gpu_usage_change = gpu_usage_after - gpu_usage_before
    #         cpu_usages.append(cpu_usage_change)
    #         ram_usages.append(ram_usage_change)
    #         gpu_usages.append(gpu_usage_change)
            timestamps.append(cycle)
            
            
    # plot_and_save_results(timestamps, cpu_usages, ram_usages, gpu_usages)
    vidcap1.release()
    vidcap2.release()
    vidcap3.release()
    
    draw_detection_plot(timestamps, detection_time_list1,'Detection', 1)
    draw_processing_plot(timestamps, data_processing_time_list1, 'Data Processing', 1)
    draw_detection_plot(timestamps, detection_time_list2,'Detection', 2)
    draw_processing_plot(timestamps, data_processing_time_list2, 'Data Processing', 2)
    draw_detection_plot(timestamps, detection_time_list3, 'Detection', 3)
    draw_processing_plot(timestamps, data_processing_time_list3, 'Data Processing',3)
    
    total_detection_time = [a + b + c for a,b,c in zip(detection_time_list1, detection_time_list2, detection_time_list3)]
    total_processing_time = [a + b + c for a,b,c in zip(data_processing_time_list1, data_processing_time_list2, data_processing_time_list3)]
    total_excute_time = [d + p for d, p in zip(total_detection_time,total_processing_time)]
    
    draw_detection_plot(timestamps, total_detection_time,'Detection', 4)
    draw_processing_plot(timestamps, total_processing_time, 'Data Processing', 4)
    
    draw_detection_plot(timestamps, total_excute_time,'Detection', 5)
    
    
    
    
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
