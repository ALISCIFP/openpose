import base64
import json
import requests
import os
import glob

def base64_from_fp(fp_img):
    with open(fp_img, "rb") as fid:
        data = fid.read()

    b64_bytes = base64.b64encode(data)
    return b64_bytes

frames_dir='/export/zs/data/jdd/zs_jd/frames'
savedir='/export/zs/data/jdd/zs_jd'

if not os.path.exists(savedir):
	os.makedirs(savedir)
if not os.path.exists(savedir + '/keypoints_all'):
	os.makedirs(savedir + '/keypoints_all')


print('----------------- Loading Frames -----------------')

frames = sorted([f for f in glob.glob(frames_dir + "/*.jpg")])
print (frames[0])
NumFrames = len(frames)
print('----------------- All Loaded -----------------', NumFrames)
n = 0
while n <= NumFrames:
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