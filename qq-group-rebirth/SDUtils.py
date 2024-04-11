from PIL import Image
import httpx
from io import BytesIO
import webuiapi
import base64
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from typing import Tuple, List
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageSegment,GroupMessageEvent
from .utils import order_member_by_time_dsa
import random
from nonebot import get_bot
from nonebot.exception import ActionFailed

class SDUtils:

    def __init__(self, sd_host: str, sd_port: int):
        self.host = sd_host
        self.port = sd_port
        self.model = 'wd-v1-4-moat-tagger.v2'
        self.threshold = 0.35
        self.protocol = "http"

    async def download_img(self, img_url: str) -> Tuple[JpegImageFile, str]:
        """通过url下载图片,返回base64 str

        Parameters
        ----------
        img_url : str
            img链接

        Returns
        -------
        Tuple[JpegImageFile, str]
            base64格式图片和PIL图片组成的tuple
        """
        with httpx.Client() as client:
            response = client.get(img_url)
            if response.status_code != 200:
                print(f"下载失败，错误代码：{response.status_code}")
        pil_image = Image.open(BytesIO(response.content))
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return pil_image, image_base64

    async def img2tags(self, img_base64: str) -> str:
        """将图像转换为tag
        Parameters
        ----------
        img_base64 : str
            base64格式image

        Returns
        -------
        str
            tags,用作后面img2img的prompt
        """
        api = "/tagger/v1/interrogate"
        url = f"{self.protocol}://{self.host}:{self.port}{api}"
        data = {
            "image": img_base64,
            "model": self.model,
            "threshold": self.threshold
        }
        # Get tags and serialize
        json_data = httpx.post(url, json=data).json()
        # 取出tags, 并拼接为str
        caption_dict = json_data['caption']['tag'].keys()
        caption_str = ', '.join(caption_dict)
        return caption_str

    async def img2img(self, tags: str, img_pil: JpegImageFile) -> JpegImageFile:
        """通过tag和原始图像生成新图像

        Parameters
        ----------
        tags : str
            img2tag反推得到的tags
        img_pil : JpegImageFile
            原始PIL格式图像
        Returns
        -------
        bytes
            bytes图像
        """
        negative_prompt = (
            "nsfw,logo,text,badhandv4,EasyNegative,"
            "ng_deepnegative_v1_75t,rev2-badprompt,"
            "verybadimagenegative_v1.3,negative_hand-neg,"
            "mutated hands and fingers,poorly drawn face,"
            "extra limb,missing limb,disconnected limbs,"
            "malformed hands,ugly,strange fingers"
        )
        api = webuiapi.WebUIApi(host=self.host, port=self.port)
        result = api.img2img(
            images=[img_pil], prompt=tags, negative_prompt=negative_prompt, seed="-1", cfg_scale=6.5, denoising_strength=0.6)
        # 获取pil图像
        result_img = result.image
        # # 将 PIL 图像对象转换为字节
        # img_byte_array = BytesIO()
        # result_img.save(img_byte_array, format='PNG')
        # result_bytes = img_byte_array.getvalue()
        return result_img

    async def combine4p(self, images: List[JpegImageFile]) -> BytesIO:
        """将4张图拼接一起

        Parameters
        ----------
        images : List[JpegImageFile]
            images数组,包含4张images

        Returns
        -------
        BytesIO
            _description_
        """
        x_offset = 0
        y_offset = 0
        combined_image = Image.new('RGB', (1024, 1024))
        for image in images:
            combined_image.paste(image, (x_offset, y_offset))
            x_offset += 512
            if x_offset >= 1024:
                x_offset = 0
                y_offset += 512
        img_byte_array = BytesIO()
        # combined_image.show()
        combined_image.save(img_byte_array, format='PNG')
        # combined_image_bytes = img_byte_array.getvalue()
        # 消息段img只接受bytesIO
        return img_byte_array

    # @staticmethod
    async def generate_ai_image_msg(self, group_id: int) -> Message:
        member_list = await get_bot("1141560393").call_api("get_group_member_list", group_id=group_id, no_cache=True)
        # 选择最近发言10人
        top10_list = order_member_by_time_dsa(member_list)

        # 随机抽取一人
        selected_user = random.choice(top10_list)
        avatar_url = f"https://q2.qlogo.cn/headimg_dl?dst_uin={selected_user['user_id']}&spec=640"
        pil_image, image_base64 = await self.download_img(avatar_url)
        tags = await self.img2tags(image_base64)
        images = []
        # 生成4张图片
        for _ in range(4):
            img_new = await self.img2img(tags, pil_image)
            images.append(img_new)
        image_BytesIO = await self.combine4p(images)
        text = (f"""信徒抽取中(10/10)...:
{[(user['user_id'], user['nickname']) for user in top10_list]}
""")
        # 消息段只接受BytesIO, 理论上也支持bytes，但懒得看了
        img_byte_array = BytesIO()
        pil_image.save(img_byte_array, format='PNG')
        msg = Message([MessageSegment.text(text)])
        msg.append(MessageSegment.text(
            f"\n少女祈祷中...\n将被重生的人为: {selected_user['nickname']}\n"))
        msg.append(MessageSegment.image(img_byte_array))
        msg.append(MessageSegment.text(f"\n重生中...\n\n新造的人:\n"))
        msg.append(MessageSegment.image(image_BytesIO))
        return msg
