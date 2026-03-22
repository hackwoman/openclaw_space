#!/usr/bin/env python3
"""Pillow 绘画能力展示"""

from PIL import Image, ImageDraw, ImageFont
import math

# ============ 1. 渐变背景 + 卡通角色 ============
def create_gradient_cartoon():
    width, height = 500, 400
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # 渐变背景
    for y in range(height):
        r = int(100 + (y / height) * 100)
        g = int(150 + (y / height) * 80)
        b = int(200 + (y / height) * 55)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 地面
    draw.ellipse([0, 320, 500, 450], fill=(100, 180, 100))
    
    # 身体
    draw.ellipse([180, 180, 320, 320], fill=(255, 107, 107))
    draw.ellipse([195, 200, 305, 300], fill=(255, 182, 182))
    
    # 眼睛
    draw.ellipse([200, 150, 240, 195], fill='white', outline='black', width=2)
    draw.ellipse([260, 150, 300, 195], fill='white', outline='black', width=2)
    draw.ellipse([210, 160, 230, 185], fill='black')
    draw.ellipse([270, 160, 290, 185], fill='black')
    draw.ellipse([215, 163, 222, 172], fill='white')
    draw.ellipse([275, 163, 282, 172], fill='white')
    
    # 嘴巴
    draw.arc([215, 200, 285, 250], 0, 180, fill='black', width=3)
    
    # 腮红
    draw.ellipse([175, 200, 205, 225], fill=(255, 182, 193, 128))
    draw.ellipse([295, 200, 325, 225], fill=(255, 182, 193, 128))
    
    # 天线
    draw.line([210, 150, 180, 80], fill=(255, 107, 107), width=6)
    draw.line([290, 150, 320, 80], fill=(255, 107, 107), width=6)
    draw.ellipse([168, 65, 192, 90], fill=(255, 215, 0), outline='black')
    draw.ellipse([308, 65, 332, 90], fill=(255, 215, 0), outline='black')
    
    # 钳子
    draw.ellipse([100, 200, 160, 280], fill=(255, 107, 107), outline='black', width=2)
    draw.ellipse([340, 200, 400, 280], fill=(255, 107, 107), outline='black', width=2)
    
    # 腿
    for x_offset in [190, 215, 285, 310]:
        draw.line([x_offset, 310, x_offset - 10, 370], fill=(255, 107, 107), width=8)
    
    # 文字
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    draw.text((150, 30), "Hello! I'm OpenClaw", fill='white', font=font)
    
    img.save('/home/kui/.openclaw/workspace/pillow_cartoon.png')
    print("✅ 卡通角色已保存: pillow_cartoon.png")

# ============ 2. 像素艺术 ============
def create_pixel_art():
    width, height = 320, 320
    img = Image.new('RGB', (width, height), '#87CEEB')
    draw = ImageDraw.Draw(img)
    
    pixel_size = 20
    
    # 像素风格的 OpenClaw
    pixels = [
        # 天线 (金色)
        ([4, 0], '#FFD700'), ([5, 0], '#FFD700'),
        ([4, 1], '#FFD700'), ([5, 1], '#FFD700'),
        ([11, 0], '#FFD700'), ([12, 0], '#FFD700'),
        ([11, 1], '#FFD700'), ([12, 1], '#FFD700'),
        # 天线杆
        ([4, 2], '#FF6B6B'), ([5, 2], '#FF6B6B'),
        ([11, 2], '#FF6B6B'), ([12, 2], '#FF6B6B'),
        ([4, 3], '#FF6B6B'), ([5, 3], '#FF6B6B'),
        ([11, 3], '#FF6B6B'), ([12, 3], '#FF6B6B'),
        # 头部
        ([5, 4], '#FF6B6B'), ([6, 4], '#FF6B6B'), ([7, 4], '#FF6B6B'), ([8, 4], '#FF6B6B'), ([9, 4], '#FF6B6B'), ([10, 4], '#FF6B6B'),
        ([4, 5], '#FF6B6B'), ([5, 5], '#FF6B6B'), ([6, 5], '#FF6B6B'), ([7, 5], '#FF6B6B'), ([8, 5], '#FF6B6B'), ([9, 5], '#FF6B6B'), ([10, 5], '#FF6B6B'), ([11, 5], '#FF6B6B'),
        ([4, 6], '#FF6B6B'), ([5, 6], '#FF6B6B'), ([6, 6], '#FF6B6B'), ([7, 6], '#FF6B6B'), ([8, 6], '#FF6B6B'), ([9, 6], '#FF6B6B'), ([10, 6], '#FF6B6B'), ([11, 6], '#FF6B6B'),
        ([4, 7], '#FF6B6B'), ([5, 7], '#FF6B6B'), ([6, 7], '#FF6B6B'), ([7, 7], '#FF6B6B'), ([8, 7], '#FF6B6B'), ([9, 7], '#FF6B6B'), ([10, 7], '#FF6B6B'), ([11, 7], '#FF6B6B'),
        # 眼睛
        ([5, 5], 'white'), ([6, 5], 'white'), ([9, 5], 'white'), ([10, 5], 'white'),
        ([5, 6], 'black'), ([6, 6], 'black'), ([9, 6], 'black'), ([10, 6], 'black'),
        # 身体
        ([5, 8], '#FF6B6B'), ([6, 8], '#FF6B6B'), ([7, 8], '#FF6B6B'), ([8, 8], '#FF6B6B'), ([9, 8], '#FF6B6B'), ([10, 8], '#FF6B6B'),
        ([4, 9], '#FF6B6B'), ([5, 9], '#FFB6B6'), ([6, 9], '#FFB6B6'), ([7, 9], '#FFB6B6'), ([8, 9], '#FFB6B6'), ([9, 9], '#FFB6B6'), ([10, 9], '#FF6B6B'),
        ([4, 10], '#FF6B6B'), ([5, 10], '#FFB6B6'), ([6, 10], '#FFB6B6'), ([7, 10], '#FFB6B6'), ([8, 10], '#FFB6B6'), ([9, 10], '#FFB6B6'), ([10, 10], '#FF6B6B'),
        ([4, 11], '#FF6B6B'), ([5, 11], '#FFB6B6'), ([6, 11], '#FFB6B6'), ([7, 11], '#FFB6B6'), ([8, 11], '#FFB6B6'), ([9, 11], '#FFB6B6'), ([10, 11], '#FF6B6B'),
        ([5, 12], '#FF6B6B'), ([6, 12], '#FF6B6B'), ([7, 12], '#FF6B6B'), ([8, 12], '#FF6B6B'), ([9, 12], '#FF6B6B'), ([10, 12], '#FF6B6B'),
        # 钳子
        ([2, 9], '#FF6B6B'), ([3, 9], '#FF6B6B'), ([12, 9], '#FF6B6B'), ([13, 9], '#FF6B6B'),
        ([1, 10], '#FF6B6B'), ([2, 10], '#FF6B6B'), ([13, 10], '#FF6B6B'), ([14, 10], '#FF6B6B'),
        ([1, 11], '#FF6B6B'), ([2, 11], '#FF6B6B'), ([13, 11], '#FF6B6B'), ([14, 11], '#FF6B6B'),
        # 腿
        ([5, 13], '#FF6B6B'), ([6, 13], '#FF6B6B'), ([9, 13], '#FF6B6B'), ([10, 13], '#FF6B6B'),
        ([4, 14], '#FF6B6B'), ([5, 14], '#FF6B6B'), ([10, 14], '#FF6B6B'), ([11, 14], '#FF6B6B'),
    ]
    
    for (x, y), color in pixels:
        draw.rectangle([x*pixel_size, y*pixel_size, (x+1)*pixel_size-1, (y+1)*pixel_size-1], fill=color)
    
    img.save('/home/kui/.openclaw/workspace/pixel_openclaw.png')
    print("✅ 像素艺术已保存: pixel_openclaw.png")

# ============ 3. 彩虹渐变圆形 ============
def create_rainbow_circle():
    width, height = 400, 400
    img = Image.new('RGB', (width, height), '#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = width // 2, height // 2
    max_radius = 150
    
    # 绘制彩虹渐变圆环
    for i in range(max_radius, 0, -1):
        ratio = i / max_radius
        r = int(255 * ratio)
        g = int(100 * (1 - ratio))
        b = int(255 * (1 - ratio))
        draw.ellipse([center_x-i, center_y-i, center_x+i, center_y+i], fill=(r, g, b))
    
    # 中心文字
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    draw.text((center_x-80, center_y-20), "Pillow!", fill='white', font=font)
    
    img.save('/home/kui/.openclaw/workspace/rainbow_circle.png')
    print("✅ 彩虹渐变已保存: rainbow_circle.png")

# ============ 4. 星空背景 ============
def create_starry_night():
    import random
    width, height = 500, 400
    img = Image.new('RGB', (width, height), '#0a0a2e')
    draw = ImageDraw.Draw(img)
    
    # 绘制星星
    random.seed(42)
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 4)
        brightness = random.randint(150, 255)
        draw.ellipse([x, y, x+size, y+size], fill=(brightness, brightness, brightness))
    
    # 绘制月亮
    draw.ellipse([350, 50, 420, 120], fill='#FFD700')
    draw.ellipse([365, 45, 430, 110], fill='#0a0a2e')
    
    # 绘制 OpenClaw 轮廓
    draw.ellipse([180, 180, 320, 320], fill='#FF6B6B', outline='#FFD700', width=3)
    draw.ellipse([200, 150, 240, 190], fill='white')
    draw.ellipse([260, 150, 300, 190], fill='white')
    draw.ellipse([210, 160, 230, 180], fill='black')
    draw.ellipse([270, 160, 290, 180], fill='black')
    draw.arc([210, 220, 290, 260], 0, 180, fill='black', width=3)
    
    # 文字
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()
    draw.text((150, 350), "✨ OpenClaw in the Stars ✨", fill='#FFD700', font=font)
    
    img.save('/home/kui/.openclaw/workspace/starry_openclaw.png')
    print("✅ 星空艺术已保存: starry_openclaw.png")

# 运行所有演示
if __name__ == '__main__':
    print("🎨 开始 Pillow 绘画演示...")
    create_gradient_cartoon()
    create_pixel_art()
    create_rainbow_circle()
    create_starry_night()
    print("\n🎉 所有作品完成！")
