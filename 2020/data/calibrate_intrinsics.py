from pathlib import Path

import numpy as np
import cv2

if __name__ == '__main__':

    img_dir = Path('calib_imgs')
    fnames = [str(f) for f in img_dir.glob('*.png')]
    fnames.sort()

    pattern_width = 8
    pattern_height = 27
    diagonal_dist = (30e-3)#*(39.37)
    pattern_size = (pattern_width, pattern_height)
    horizontal_grid_dist = 2*diagonal_dist/np.sqrt(2)
    #print('Diagonal_dist:{} {}'.format(diagonal_dist, horizontal_grid_dist))

    corners = list()

    for row in range(pattern_height):
        for col in range(pattern_width):
            x = (col*2+(row%2))*horizontal_grid_dist
            y = (row * horizontal_grid_dist)
            corners.append(np.array([x,y,0]).reshape(1,3).astype(np.float32))

    corners = np.vstack(corners).reshape(-1,3)
    img_centers = list()
    obj_pts = list()
    for f in fnames:
        obj_pts.append(corners)
        img = cv2.imread(f)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        ret, centers = cv2.findCirclesGrid(gray, pattern_size, None, cv2.CALIB_CB_ASYMMETRIC_GRID)
        if ret:
            img_centers.append(centers)


    retval, cam_mtx, dist_coeff, rvecs, tvecs = cv2.calibrateCamera(obj_pts, img_centers,(gray.shape[1], gray.shape[0]),None,None)  

    cam_data = {'cam_mtx':cam_mtx, 'dist_coeff':dist_coeff}
    print(cam_data)
    print("\nReporjection Error: {}".format(retval))
