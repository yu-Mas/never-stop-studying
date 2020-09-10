from PIL import Image

class MyRandomAffine(object):
    def __init__(self,degrees,scale,pad_white=True):
        self.degrees = degrees
        self.scale = scale
    def __call__(self, img):
        # 转换为有alpha层
        scale_x = int(512 * self.scale)
        scale_y = int(512 * self.scale)
        img = img.resize((scale_x,scale_y))

        img2 = img.convert('RGBA')

        # 旋转
        rot = img2.rotate(self.degrees, expand=1)

        # 创建一个与旋转图像大小相同的白色图像
        if img.mode == 'RGB':
            fff = Image.new('RGBA', rot.size, (255,)*4)
        elif img.mode == 'L':
            fff = Image.new('RGBA', rot.size, (0,)*4)
        # 使用alpha层的rot作为掩码创建一个复合图像
        out = Image.composite(rot, fff, rot)
        out_x,out_y = out.size[0],out.size[1]
        # 保存
        if out_x <= 512:
            out = out.convert(img.mode).resize((512,512))
        elif out_x > 512:
            out = out.convert(img.mode).crop((out_x//2-256,out_y//2-256,out_x//2+256,out_y//2+256))
        assert out.size == (512,512)
        out.save('data/train/crop/temp/temp2/1.png')
        return out