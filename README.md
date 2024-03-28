# Camera Calibration

## Project Overview
This repository contains the code and documentation for 2 different pipelines for calibrating two different cameras, one using a Direct Linear Transform and the other using inbuilt OpenCV functions

## Problem 1: Camera Calibration

### Overview

This problem focuses on calibrating the camera mathematically using Direct Linear Transform (DLT) and decomposing the projection matrix to obtain the intrinsic matrix \( K \), rotation matrix \( R \), and translation vector \( T \).

### Pipeline

1. **P Matrix Calculation:**
   - Construct the \( A \) matrix by stacking 2 rows for every point to form a matrix of shape \( (16 \times 12) \).
   - Apply Singular Value Decomposition (SVD) on \( A \) to obtain \( U \), \( S \), and \( V \).
   - Extract the last row of \( V \) corresponding to the smallest eigenvalue and reshape it into a \( (3 \times 4) \) matrix, which represents the \( P \) matrix.

![image](https://github.com/Shyam-pi/Camera-Calibration/assets/57116285/cfc11146-380b-4f9b-99f1-ecec10d0ac64)


2. **Decomposition of \( P \):**
   - Perform RQ decomposition on the left \( 3 \times 3 \) matrix of \( P \) using the Gram-Schmidt method to obtain the intrinsic matrix \( K \) and the rotation matrix \( R \).
   - Compute the translation vector \( T \) as \( (KR)^{-1} \cdot P[:,3] \), where \( P[:,3] \) represents the last column of \( P \).
  
![image](https://github.com/Shyam-pi/Camera-Calibration/assets/57116285/edb58409-9a28-4040-9d5f-e5e4553e360d)

3. **Reprojection Error Calculation:**
   - Compute the reprojection error for each point using the decomposed matrices and compare it against the original image points.

![image](https://github.com/Shyam-pi/Camera-Calibration/assets/57116285/02bb8e3a-e72f-406b-a089-e49df8e175ea)


### Code

The code for Problem 1 is available in the `prob1.py` file.

## Problem 2: Checkerboard Corner Detection and Camera Calibration

### Overview

This problem involves detecting checkerboard corners in images, computing the reprojection error, and estimating the intrinsic matrix \( K \) using OpenCV functions.

### Pipeline

1. **Checkerboard Corner Detection:**
   - Utilize corner detection methods (e.g., OpenCV's `findChessboardCorners`) to identify the checkerboard corners in each image.
   - Display the detected corners for visualization.

![image](https://github.com/Shyam-pi/Camera-Calibration/assets/57116285/80b452ed-2e64-43b4-9a4c-22f06db92113)


2. **Reprojection Error Calculation:**
   - Compute the reprojection error for each image using built-in functions in OpenCV.

![image](https://github.com/Shyam-pi/Camera-Calibration/assets/57116285/016142ac-9520-4b77-a987-d2129a4de647)

   
3. **Intrinsic Matrix Computation:**
   - Compute the intrinsic matrix \( K \) using the detected checkerboard corners and their corresponding world coordinates.
  
![image](https://github.com/Shyam-pi/Camera-Calibration/assets/57116285/8800759b-1c88-4581-b351-290e893b74cc)


### Improving Accuracy of \( K \) Matrix

- **Use More Images:** Capture images from different angles to capture a wider range of views.
- **Larger Checkerboard:** Use a larger checkerboard to provide more calibration points per image.
- **Consistent Lighting:** Maintain consistent lighting conditions during calibration.
- **High-Quality Checkerboard:** Use a high-quality checkerboard to reduce false correspondences and subpixel measurement errors.
- **Refinement:** Employ RANSAC or discard images/points with high reprojection errors and iteratively compute \( K \).
- **Lens Distortion Correction:** Incorporate lens distortion corrections to enhance the accuracy of \( K \).
