from PIL import Image, ImageDraw
import os

# 创建一个 32x32 的图像
img = Image.new('RGB', (32, 32), color='white')
draw = ImageDraw.Draw(img)

# 绘制一个简单的 "P" 字母
draw.text((8, 4), "P", fill='black', font=None)

# 确保 static 目录存在
os.makedirs('static', exist_ok=True)

# 保存为 ICO 文件
img.save('static/favicon.ico') 