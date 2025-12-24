import base64
import random
import string
from io import BytesIO

from captcha.image import ImageCaptcha


# 生成图片验证码
def generate_captcha_image(img_format="PNG"):
    """
    生成图片验证码
    :return: 验证码base64格式图片
    """
    chars = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    img = ImageCaptcha(width=120, height=40, font_sizes=tuple([30])).generate_image(chars)
    buf = BytesIO()
    img.save(buf, format=img_format)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return {
        "image": f"data:image/{img_format.lower()};base64,{b64}",
        "code": chars.lower()
    }
