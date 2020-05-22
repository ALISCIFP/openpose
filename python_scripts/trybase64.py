import base64
from io import BytesIO

from PIL import Image


def img_arr_from_base64(b64_bytes):
    image_bytes = BytesIO(base64.b64decode(b64_bytes))
    im = Image.open(image_bytes)
    return im


def base64_from_fp(fp_img):
    with open(fp_img, "rb") as fid:
        data = fid.read()

    b64_bytes = base64.b64encode(data)
    return b64_bytes


if __name__ == '__main__':
    fp_img = "../../examples/media/COCO_val2014_000000000241.jpg"
    base64_bytes = base64_from_fp(fp_img)
    im = img_arr_from_base64(base64_bytes)
    # im = Image.fromarray(np.array(im)[:,:,::-1])
    im.save("ji.jpg")
    import pdb

    pdb.set_trace()
