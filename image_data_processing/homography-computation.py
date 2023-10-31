import numpy as np
import cv2 as cv

drawing = False # true if mouse is pressed
src_x, src_y = -1,-1
dst_x, dst_y = -1,-1

src_list = [];
dst_list = [];

# mouse callback function
def select_points_src(event,x,y,flags,param):
    global src_x, src_y, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        src_x, src_y = x,y
        cv.circle(src_copy,(x,y),5,(0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False

# mouse callback function
def select_points_dst(event,x,y,flags,param):
    global dst_x, dst_y, drawing
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        dst_x, dst_y = x,y
        cv.circle(dst_copy,(x,y),5,(0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False

def get_plan_view(src, dst):
    src_pts = np.array(src_list).reshape(-1,1,2)
    dst_pts = np.array(dst_list).reshape(-1,1,2)
    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
    # H = np.array([[-1.36907887e-02,-1.45784955e-01,5.85560938e+02],
    #               [2.74205048e-01,4.99892124e-01,-3.81723625e+02],
    #               [-1.09736260e-04,2.32056792e-03,1.00000000e+00]])
    # H = np.array([[-1.36907887e-02, -1.45784955e-01, 5.85560938e+02],  # Step 2: Convert H to NumPy array
    #               [2.74205048e-01, 4.99892124e-01, -3.81723625e+02],
    #               [-1.09736260e-04, 2.32056792e-03, 1.00000000e+00]])
    print("H:")
    print(H)
    plan_view = cv.warpPerspective(src, H, (dst.shape[1], dst.shape[0]))
    return plan_view

def merge_views(src, dst):
    plan_view = get_plan_view(src, dst)
    for i in range(0,dst.shape[0]):
        for j in range(0, dst.shape[1]):
            if(plan_view.item(i,j,0) == 0 and \
               plan_view.item(i,j,1) == 0 and \
               plan_view.item(i,j,2) == 0):
                plan_view.itemset((i,j,0),dst.item(i,j,0))
                plan_view.itemset((i,j,1),dst.item(i,j,1))
                plan_view.itemset((i,j,2),dst.item(i,j,2))
    return plan_view;

# src = cv.imread('./largeCoordinate.png', -1)
# src_copy = src.copy()

src = cv.imread('./sang_detect.jpeg', -1)

height, width = src.shape[:2]

# Step 2: Resize 'src' to have the same dimensions as 'src2'
#src = cv.resize(src, (width2, height2))
resize_factor = 0.5  # Change this value to your desired resize factor (e.g., 0.5 for half size)
src = cv.resize(src, (int(width * resize_factor), int(height * resize_factor)))
src_copy = src.copy()

cv.namedWindow('src')
cv.moveWindow("src", 80,80);
cv.setMouseCallback('src', select_points_src)

dst = cv.imread('./roomMap.png', -1)
dst_copy = dst.copy()
cv.namedWindow('dst')
cv.moveWindow("dst", 780,80);
cv.setMouseCallback('dst', select_points_dst)

while(1):
    cv.imshow('src',src_copy)
    cv.imshow('dst',dst_copy)
    k = cv.waitKey(1) & 0xFF
    if k == ord('s'):
        print('save points')
        cv.circle(src_copy,(src_x,src_y),5,(0,255,0),-1)
        cv.circle(dst_copy,(dst_x,dst_y),5,(0,255,0),-1)
        src_list.append([src_x,src_y])
        dst_list.append([dst_x,dst_y])
        print("src points:")
        print(src_list);
        print("dst points:")
        print(dst_list);
    elif k == ord('h'):
        print('create plan view')
        plan_view = get_plan_view(src, dst)
        cv.imshow("plan view", plan_view) 
    elif k == ord('m'):
        print('merge views')
        merge = merge_views(src,dst)      
        cv.imshow("merge", merge)        
    elif k == 27:
        break
cv.destroyAllWindows()

