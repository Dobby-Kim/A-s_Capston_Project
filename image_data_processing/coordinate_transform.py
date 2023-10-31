import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# label 숫자 정보에 따른 정보
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

# Function to transform normalized coordinates
def transform_coordinates_normalized(coordinates, mtrx, src_shape, dst_shape):
    transformed_coordinates = []
    for coord in coordinates:
        # Normalize coordinates according to source image dimensions
        x_norm, y_norm = coord[0] * src_shape[1], coord[1] * src_shape[0]
        
        # Convert to homogeneous coordinates
        homogeneous_coord = np.array([x_norm, y_norm, 1])
        
        # Apply transformation
        transformed_coord = np.dot(mtrx, homogeneous_coord)
        
        # Convert back to 2D coordinates
        transformed_coord = transformed_coord / transformed_coord[2]
        
        # Denormalize according to destination image dimensions
        x_denorm, y_denorm = transformed_coord[0] / dst_shape[1], transformed_coord[1] / dst_shape[0]
        
        transformed_coordinates.append([x_denorm, y_denorm])
        
    return np.array(transformed_coordinates)

# Function to display transformed coordinates using OpenCV
def display_transformed_coordinates_opencv(image_path, transformed_coordinates, labels, label_map, dst_shape):
    dst_image = cv2.imread(image_path)
    for coord in transformed_coordinates:
        x, y = int(coord[0] * dst_shape[1] * 0.95 ), int(coord[1] * dst_shape[0] * 0.87)
        cv2.circle(dst_image, (x, y), 5, (0, 0, 255), -1)
    print(transformed_coordinates)
    cv2.imshow('Transformed Coordinates', dst_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function to display transformed coordinates using Matplotlib
def display_transformed_coordinates_matplotlib(image_path, transformed_coordinates, labels, label_map, dst_shape):
    img = mpimg.imread(image_path)
    x_coords = [coord[0] * dst_shape[1] * 0.95 for coord in transformed_coordinates]
    y_coords = [coord[1] * dst_shape[0] * 0.87 for coord in transformed_coordinates]
    print(transformed_coordinates)
    plt.imshow(img)
    plt.scatter(x_coords, y_coords, c='red')
    
    for i, label in enumerate(labels):
        plt.text(x_coords[i], y_coords[i], label_map[label], fontsize=12, ha='right', va='bottom')
    plt.show()

#!############################# Example Usage #######################################
H = np.array([[5.60419376e-01, 9.71581689e-01, -3.79450113e+02],
            [-3.39450669e-02, 1.77097300e+00, -2.56173657e+02],
            [-1.75642895e-04, 4.53427216e-03, 1.00000000e+00]])

original_data = [
    [24, 0.05539143458008766, 0.5086705088615417, 0.10960118472576141, 0.2543352544307709],
    [67, 0.8231905698776245, 0.4282711446285248, 0.022156573832035065, 0.0262743029743433],
    [26, 0.1759231835603714, 0.39306357502937317, 0.060561299324035645, 0.14503414928913116],
    [63, 0.6816838979721069, 0.46295323967933655, 0.07415066659450531, 0.05570152401924133],
    [24, 0.7562776803970337, 0.38596951961517334, 0.0762186124920845, 0.06673672795295715],
    [63, 0.5094534754753113, 0.5806621313095093, 0.07769571989774704, 0.10930110514163971],
    [24, 0.7100443243980408, 0.1886495053768158, 0.04697193577885628, 0.07882291078567505],
    [0, 0.7590842247009277, 0.2320021092891693, 0.07474150508642197, 0.20861797034740448],
    [63, 0.4311669170856476, 0.17682605981826782, 0.04224519804120064, 0.05202312022447586]
]
original_labels = [item[0] for item in original_data]


src_image_path = './largeCoordinate.png'
dst_image_path = './roomMap.png'
src = cv2.imread(src_image_path, -1)
dst = cv2.imread(dst_image_path, -1)

#!###################################################################################

src_shape = (src.shape[0] , src.shape[1])
dst_shape = (dst.shape[1] , dst.shape[0]) 

original_coordinates = np.array([[item[1], item[2]] for item in original_data])
transformed_coordinates = transform_coordinates_normalized(original_coordinates, H, src_shape, dst_shape)

display_transformed_coordinates_opencv(dst_image_path, transformed_coordinates, original_labels, label_map, dst_shape)
display_transformed_coordinates_matplotlib(dst_image_path, transformed_coordinates, original_labels, label_map, dst_shape)

