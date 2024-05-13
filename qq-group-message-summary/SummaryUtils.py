from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import zoneinfo
from nonebot import require
require("nonebot_plugin_chatrecorder")
from nonebot_plugin_chatrecorder import get_messages_plain_text
from datetime import datetime, timedelta


class Summary:
    """获取聊天记录，并生成聊天摘要
    """

    def __init__(self, plugin_config, qq_group_id,prompt):
        self.client = OpenAI(
            api_key=plugin_config.ai_secret_key,
            base_url="https://api.atomecho.cn/v1",
        )
        self.keywords_file_path = plugin_config.keywords_file_path
        self.exclude_id1s = plugin_config.exclude_user_list
        self.qq_group_id = qq_group_id
        self.prompt = prompt
# Get records:

    async def _get_message(self) -> list:
        """获取消息记录
        返回值:
        * ``List``: 消息记录列表
        """
        beijing_tz = zoneinfo.ZoneInfo("Asia/Shanghai")
        exclude_id1s = self.exclude_id1s
        records = await get_messages_plain_text(
            exclude_id1s=exclude_id1s,
            id2s=[self.qq_group_id],
            time_start=datetime.now(beijing_tz).replace(hour=0),
            time_stop=datetime.now(beijing_tz).replace(hour=22),
        )
        return records

# get ai message:
    async def get_ai_message_res(self, message: str) -> ChatCompletion:
        """异步获取AI回复消息的结果。

        参数:
        message (str): 需要AI进行响应的用户消息文本。

        返回值:
        ChatCompletion: AI生成的聊天回复内容。
        """
        content = "如下是一段多个用户参与的聊天记录,请提取有意义的词句，"+self.prompt+":" + message
        # content_list = await self._content_cutting(content)
        response = self.client.chat.completions.create(
            model="Llama3-Chinese-8B-Instruct",
            messages=[
                {"role": "user", "content": content}
            ],
            temperature=0.3,
            stream=False
        )
        return response

    async def _generate_ai_message(self, content_cut_origin_record) -> str:
        """逐段生成ai总结，并计算token
        """
        if len(content_cut_origin_record) > 1:
            ai_summarization = ""
            used_tokens = ""
            for record in content_cut_origin_record:
                response = await self.get_ai_message_res(record)
                ai_summary = response.choices[0].message.content
                ai_summarization = ai_summary+"\n===分割===\n"+ai_summarization
                used_token = response.usage
                used_tokens = used_tokens+str(used_token)
                print(f"Staging Completed!")
        else:
            response = await self.get_ai_message_res(content_cut_origin_record[0])
            ai_summary = response.choices[0].message.content
            ai_summarization = ai_summary
            used_token = response.usage
            used_tokens = str(used_token)
            print(f"Staging Completed!")
        return ai_summarization, used_tokens


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
        3、将切割后的消息逐段丢给ai, 并将返回结果拼起来
        4、ai结果切割
        """
        record = await self._get_message()
        content_filter = await self.filter(record)
        content_cut_origin_record = await self._content_cutting(content_filter, max_byte_size=3000)
        # 3、生成并拼接ai总结
        # 如果content_cut_origin_record为空,则返回数据不足
        if content_cut_origin_record == [""]:
            ai_summarization_cut = ["数据不足"]
            used_tokens = "数据不足"
        else:
            ai_summarization, used_tokens = await self._generate_ai_message(
                content_cut_origin_record)
            # 4、ai结果切割
            ai_summarization_cut = await self._content_cutting(ai_summarization, max_byte_size=10000)

        return ai_summarization_cut, used_tokens
