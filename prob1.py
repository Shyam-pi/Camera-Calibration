import numpy as np
import scipy

image_pts = np.array([  [756, 213],
                        [758, 415],
                        [758, 686],
                        [759, 966], 
                        [1190, 172],
                        [329, 1041],
                        [1204, 850],
                        [340, 159]  ])

world_pts = np.array([  [0, 0, 0],
                        [0, 3, 0],
                        [0, 7, 0],
                        [0, 11, 0], 
                        [7, 1, 0],
                        [0, 11, 7],
                        [7, 9, 0],
                        [0, 1, 7]   ])

num_points = 8

N = num_points
homog_image_pts = np.hstack((image_pts, np.ones((N, 1))))
homog_world_pts = np.hstack((world_pts, np.ones((N, 1))))

# Direct linear transform
A = np.zeros((2*N, 12))

for i in range(N):
    X, Y, Z, _ = homog_world_pts[i, :]
    u, v, _ = homog_image_pts[i, :]
    
    A[2*i, :] = np.array([X, Y, Z, 1, 0, 0, 0, 0, -u*X, -u*Y, -u*Z, -u])
    A[2*i+1, :] = np.array([0, 0, 0, 0, X, Y, Z, 1, -v*X, -v*Y, -v*Z, -v])

_, _, V = np.linalg.svd(A)
P = V[-1, :].reshape((3, 4))
P_norm = P/P[-1,-1]

print(f"\nP matrix = \n{P}\n")
print(f"Normalized P matrix = \n{P_norm}\n")

# Computing K and R using rq factorization
R, Q = scipy.linalg.rq(P[:,:-1])
T = -1 * np.linalg.inv(P[:,:-1]) @ P[:,-1]

K = R # Upper triangle matrix R gives the intrinsic matrix K
R = Q # Orthonormal matrix Q is the rotation matrix R

print(f"\nNormalized Intrinsic matrix = \n{K/K[-1,-1]}\n")
print(f"Rotation matrix = \n{R}\n")
print(f"Translation vector = \n{T}\n")

# Calculate reprojection error
reproj_err = 0
for i in range(num_points):
    # Project 3D point onto image plane with denormalized P matrix
    projected_pt = P_norm @ np.append(world_pts[i], 1)
    projected_pt /= projected_pt[2]

    # calculate Euclidean distance between actual and projected 2D points
    err = np.linalg.norm(image_pts[i] - projected_pt[:2])
    print(f"Reprojection error for point {i + 1} = {err}")

print("\n")