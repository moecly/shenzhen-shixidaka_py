from PIL import Image

# 打开验证码图片
captcha_image = Image.open('test.png')  # 替换为你的验证码图片路径

# 显示验证码图片
captcha_image.show()
