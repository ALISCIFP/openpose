# From Python
# It requires OpenCV installed for Python
import base64
import json
import sys
from io import BytesIO

import cv2
import numpy as np
from PIL import Image

# Import Openpose (Windows/Ubuntu/OSX)
sys.path.append("/openpose/build/python/openpose/")
import pyopenpose as op

# Flags
# parser = argparse.ArgumentParser()
# parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000241.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
# args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/openpose/models/"
params["face"] = True
params["hand"] = True

# Add others in path?
# for i in range(0, len(args[1])):
#     curr_item = args[1][i]
#     if i != len(args[1])-1: next_item = args[1][i+1]
#     else: next_item = "1"
#     if "--" in curr_item and "--" in next_item:
#         key = curr_item.replace('-','')
#         if key not in params:  params[key] = "1"
#     elif "--" in curr_item and "--" not in next_item:
#         key = curr_item.replace('-','')
#         if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()


def get_openpose_from_fp(fp_img):
    img_arr = cv2.imread(fp_img)
    return get_openpose(img_arr)


def img_arr_from_base64(b64_bytes):
    image_bytes = BytesIO(base64.b64decode(b64_bytes))
    im = Image.open(image_bytes)
    im_arr = np.array(im )
    return im_arr


def base64_from_fp(fp_img):
    with open(fp_img, "rb") as fid:
        data = fid.read()

    b64_bytes = base64.b64encode(data)
    return b64_bytes


def render_result(pose_keypoints, face_keypoints, hand_left_keypoints, hand_right_keypoints):
    return json.dumps({
        "version": 1.2,
        "people": [
            {
                "pose_keypoints_2d": pose_keypoints,
                "face_keypoints_2d": face_keypoints,
                "hand_left_keypoints_2d": hand_left_keypoints,
                "hand_right_keypoints_2d": hand_right_keypoints,
                "pose_keypoints_3d": [],
                "face_keypoints_3d": [],
                "hand_left_keypoints_3d": [],
                "hand_right_keypoints_3d": []
            }
        ]
    })


def get_openpose(rgb_arr):
    # Process Image
    datum = op.Datum()

    datum.cvInputData = cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)
    opWrapper.emplaceAndPop([datum])

    # Display Image
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    print("Face keypoints: \n" + str(datum.faceKeypoints))
    print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
    print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
    # cv2.imwrite("out/02.jpg", datum.cvOutputData)
    # cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
    # cv2.waitKey(0)
    first_human_pose_kps = datum.poseKeypoints[0].reshape(-1).tolist()
    first_human_face_kps = datum.faceKeypoints[0].reshape(-1).tolist()
    first_human_lhand_kps = datum.handKeypoints[0][0].reshape(-1).tolist()
    first_human_rhand_kps = datum.handKeypoints[1][0].reshape(-1).tolist()

    myjson = render_result(first_human_pose_kps,
                           first_human_face_kps,
                           first_human_lhand_kps,
                           first_human_rhand_kps,
                           )
    return myjson


if __name__ == '__main__':
    fp_img = "../../../examples/media/COCO_val2014_000000000241.jpg"
    base64_str = base64_from_fp(fp_img)
    im = img_arr_from_base64(base64_str)
    im.save("ji.jpg")
    import pdb

    pdb.set_trace()

    get_openpose_from_fp("../../../examples/media/COCO_val2014_000000000241.jpg")
