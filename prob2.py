import numpy as np
import cv2
import os

# Number of boxes = (7,10), therefore num_corners = (6,9)
num_corners = (6, 9)
input_folder_path = 'Calibration_Imgs/'

# side_len = 1

side_len = 0.0215

objpts = np.zeros((num_corners[0] * num_corners[1], 3), np.float32)
objpts[:, :2] = np.mgrid[0:num_corners[0], 0:num_corners[1]].T.reshape(-1, 2)

objpoints = []  # Placeholder for 3D coordinates in world frame
imgpoints = []  # Placeholder for 2D coordinates in image frame

images = []

for filename in os.listdir(input_folder_path):
        img = cv2.imread(os.path.join(input_folder_path, filename))
        images.append(img)

# Loop through images
for i,img in enumerate(images):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Finding Corner points
        ret, corners = cv2.findChessboardCorners(gray, num_corners, None)

        if ret == True:
                objpoints.append(objpts)
                
                # Refining corners for subpixel accuaracy
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
                imgpoints.append(corners2)

                # Displaying corners
                img = cv2.drawChessboardCorners(img, num_corners, corners2, ret)
                output_folder = 'Results/'
                filename = 'img_' + str(i + 1) + '.jpg'
                cv2.imwrite(os.path.join(output_folder, filename), img)
                cv2.imshow('img', cv2.resize(img, (int(img.shape[1]*0.5), int(img.shape[0]*0.5))))
                cv2.waitKey(50)

cv2.destroyAllWindows()

# Perform camera calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Print K matrix
print("\nCamera matrix K :")
print(mtx)
print("\n")

# Reprojection error calculation
for i,img in enumerate(images):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Reproject world points to camera plane
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)

    # Calculate reprojection error
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)

    # Print reprojection error
    print(f"Reprojection error for Image {i+1}: {error}")

print("\n")