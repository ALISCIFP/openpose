import base64
import json
import requests
import os
import glob
import argparse


def base64_from_fp(fp_img):
    with open(fp_img, "rb") as fid:
        data = fid.read()

    b64_bytes = base64.b64encode(data)
    return b64_bytes
def main(args):


    if not os.path.exists(args.keypoints_dir):
        os.makedirs(args.keypoints_dir)
    if not os.path.exists(args.keypoints_dir + '/keypoints_all'):
        os.makedirs(args.keypoints_dir + '/keypoints_all')


    print('----------------- Loading Frames -----------------')

    frames = sorted([f for f in glob.glob(args.frames_dir + "/*.jpg")])
    print (frames[0])
    NumFrames = len(frames)
    print('----------------- All Loaded -----------------', NumFrames)
    n = 0
    while n < NumFrames:
        print(n)
        base64_bytes = base64_from_fp(frames[n])
        r = requests.post("http://localhost:3000/openpose", data=base64_bytes)

    # json_object = json.dumps(r.content)

    # Writing to sample.json
        frame_name = frames[n]
        filebase_name = os.path.basename(frame_name)
        filebase_name = filebase_name.split(".")[0]
        key_name = frame_name.replace("frames", "keypoints_all")
        keypoints_name = key_name.replace('.jpg',"_keypoints.json")
        with open(keypoints_name, 'w') as f:
            json.dump(r.json(), f)

        n += 1


if __name__ == "__main__":
    print('RUN sudo docker run -it --gpus 0 -p 3000:3000 --rm pyopenpse First' )
    print( "Start Keypoints script ...")

    parser = argparse.ArgumentParser(description="Video2Frames converter")
    parser.add_argument('frames_dir', metavar='<input_frames_file>', help="Input video file")
    parser.add_argument('keypoints_dir', metavar='<output_folder>', help="Output folder. If exists it will be removed")

    # frames_dir='/export/zs/data/jdd/zs_jd/frames'
    # keypointsdir='/export/zs/data/jdd/zs_jd'

    args = parser.parse_args()
    ret = main(args)
    exit(ret)