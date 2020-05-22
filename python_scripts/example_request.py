import base64

import requests


def base64_from_fp(fp_img):
    with open(fp_img, "rb") as fid:
        data = fid.read()

    b64_bytes = base64.b64encode(data)
    return b64_bytes


fp_img = "/export/zs/s2g/oliver_face70_AJ/test_img/Alex_Jones_-_Last_Week_Tonight_with_John_Oliver_HBO-WyGq6cjcc3Q_29_605_0_14_08.png"
base64_bytes = base64_from_fp(fp_img)
r = requests.post("http://localhost:3000/openpose", data=base64_bytes)
print(type(r.content))
print(r.content)
