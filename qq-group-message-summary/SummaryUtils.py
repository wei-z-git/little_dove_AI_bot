from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import zoneinfo
from nonebot import require
require("nonebot_plugin_chatrecorder")
from nonebot_plugin_chatrecorder import get_messages_plain_text
from datetime import datetime
from typing import Tuple
from openai import RateLimitError
import time
from nonebot import logger


class Summary:
    """获取聊天记录，并生成聊天摘要
    """

    def __init__(self, plugin_config, qq_group_id, prompt, resum_prompt: str = "如下是一段多个用户参与的聊天记录,请提取有意义的词句，提炼为800字以内消息:"):
        """初始化函数
        :param plugin_config: 插件配置对象，包含AI密钥、关键词文件路径和排除用户列表等配置
        :param qq_group_id: QQ群ID
        :param prompt: ai最终prompt
        :param resum_prompt:如果字数超过限制，通过此prompt进行预总结
        """        
        self.client = OpenAI(
            api_key=plugin_config.ai_secret_key,
            base_url="https://api.atomecho.cn/v1",
        )
        self.keywords_file_path = plugin_config.keywords_file_path
        self.exclude_id1s = plugin_config.exclude_user_list
        self.qq_group_id = qq_group_id
        self.prompt = prompt
        self.resum_prompt=resum_prompt

# Get records:

    async def _get_record(self) -> list:
        """获取消息记录
        返回值:
        * ``List``: 消息记录列表
        """
        beijing_tz = zoneinfo.ZoneInfo("Asia/Shanghai")
        exclude_id1s = self.exclude_id1s
        records = await get_messages_plain_text(
            exclude_id1s=exclude_id1s,
            id2s=[self.qq_group_id],
            time_start=datetime.now(beijing_tz).replace(hour=19),
            time_stop=datetime.now(beijing_tz).replace(hour=22),
        )
        return records

    async def get_ai_response_api(self, content) -> ChatCompletion:
        """调用llama api,获取AI回复消息的结果。

        参数:
        content (str): 需要AI进行响应的用户消息文本。

        返回值:
        ChatCompletion: AI生成的聊天回复内容。
        """
        max_retries = 5  # 最大重试次数
        retry_delay = 3  # 重试延迟时间（秒）
        retries = 0
        while retries < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model="Llama3-Chinese-8B-Instruct",
                    messages=[
                        {"role": "user", "content": content}
                    ],
                    temperature=0.3,
                    stream=False
                )
                print("调用llama api")
                return response
            except RateLimitError as e:
                retries += 1
                if retries >= max_retries:
                    logger.opt(exception=True).error("RateLimitError")
                    response = ChatCompletion(id="ErrorHander", choices=[{"finish_reason":"stop","index":0,"message": {"content":"未能获取","role":"assistant" }}], created=0, model="", object="chat.completion", system_fingerprint=None, usage=None)
                    return response
                logger.warning(f"retries: {retries}/{max_retries}")
                time.sleep(retry_delay)
        

    async def get_ai_response_api_message_str(self, content) -> str:
        """获取消息记录对象的内容, string
        返回值:
        * ``str``: 消息记录文本
        """
        response = await self.get_ai_response_api(content)
        response_text=response.choices[0].message.content
        return response_text
# get ai message:

    async def get_ai_message_res(self, message: str, max_byte_size=3000) -> Tuple[str, str]:
        """异步获取AI回复消息的结果, 包含token和ai message
        """
        message = await self._resummarize_message(message, max_byte_size)
        content = "如下是一段信息,请提取有意义的词句,"+self.prompt+":" + message
        response = await self.get_ai_response_api(content)
        if response and response.choices and response.choices[0].message.content:
            ai_summarization = response.choices[0].message.content
        else:
            ai_summarization = "未能生成有效的AI回复"
        used_token = str(response.usage) if response else "未使用token"
        return ai_summarization, used_token

    async def _resummarize_message(self, message: str, max_byte_size=3000) -> str:
        """将过长的消息进行重新总结为短消息
        规则: 一个汉字占3个字节,ai输入不能超过3000bytes,所以是1000字
        1.将list中每项信息压缩之1/2,
        2.再合并起来为str A
        3.判断A是否超过3000bytes,如果超过则继续压缩,直到符合
        """
        # 截取消息
        loop_count = 0
        while True:
            loop_count += 1
            message_combined = ""
            content_list = await self._content_cutting(message, max_byte_size=5000)
            logger.info(f"content_list长度:{len(content_list)}")
            for content in content_list:
                content = self.resum_prompt+content
                message_ai = await self.get_ai_response_api_message_str(content)
                message_combined = message_ai + "\n" + message_combined
            if len(message_combined.encode('utf-8')) <= max_byte_size:
                break
            else:
                message = message_combined
        logger.info(f"循环次数: {loop_count}")
        return message_combined

# Filters:

    async def _load_filter_keywords(self) -> list:
        """加载过滤关键词
        `    返回值:
        * ``List[str]``: 过滤关键词列表
        """
        filepath = self.keywords_file_path
        with open(filepath, 'r', encoding='utf-8') as file:
            keywords = file.readlines()
        # 移除每个关键词末尾的换行符
        keywords = [keyword.strip() for keyword in keywords]
        return keywords

    async def filter(self, records: list) -> str:
        """过滤消息
        Parameters:
        - records: 待过滤消息，nonebot聊天记录

        Returns:
        - 已过滤消息,一坨str, 用换行符隔开
        """
        records_list = []
        keywords = await self._load_filter_keywords()
        for record in records:
            # 1.去除空消息 2.过滤关键词
            if (record != "" and
                    all(keyword not in record for keyword in keywords)):
                records_str = f"{record}"
                records_list.append(records_str)
        records_merged = '。'.join(records_list)
        return records_merged

# Content cutting:
    async def _content_cutting(self, content: str, max_byte_size: int) -> list:
        '''将content以max_byte_size字符为单位, 分割为list,
        长度使用utf-8编码计算
        '''
        num_chunks = (len(content.encode('utf-8')) // max_byte_size) + 1
        max_chunk_size = len(content) // num_chunks
        chunks_list = []
        for chunk_number in range(num_chunks):
            # 计算当前部分的起始和结束索引
            start_index = chunk_number * max_chunk_size
            end_index = (chunk_number + 1) * max_chunk_size
            # 切割请求内容为当前部分
            current_chunk = content[start_index:end_index]
            chunks_list.append(current_chunk)
        return chunks_list

# message handle:
    async def get_length(self) -> str:
        """获取过滤后消息总长度
        """
        ai_summarization_cut, used_tokens = await self.message_handle()
        total_length = sum(len(word.encode('utf-8'))
                           for word in ai_summarization_cut)
        return total_length

    async def message_handle(self) -> tuple[list[str], str]:
        """1、处理原始消息,先过滤，
        2、然后再切割,获得切割后的消息list
        4、ai结果切割
        """
        record = await self._get_record()
        content_filter = await self.filter(record)
        # content_cut_origin_record = await self._content_cutting(content_filter, max_byte_size=3000)
        # 3、生成并拼接ai总结
        # 如果content_cut_origin_record为空,则返回数据不足
        if content_filter == "":
            ai_summarization_cut = ["数据不足"]
            used_tokens = "数据不足"
        else:
            ai_summarization, used_tokens = await self.get_ai_message_res(
                content_filter)
            # 4、ai结果切割
            ai_summarization_cut = await self._content_cutting(ai_summarization, max_byte_size=10000)

        return ai_summarization_cut, used_tokens
