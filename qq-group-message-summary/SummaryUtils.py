from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import zoneinfo
from nonebot_plugin_chatrecorder import get_message_records
from nonebot_plugin_session import SessionIdType
from datetime import datetime, timedelta
from nonebot_plugin_chatrecorder import MessageRecord


class Summary:
    """获取聊天记录，并生成聊天摘要
    """

    async def __init__(self, plugin_config, session):
        self.client = OpenAI(
            api_key=plugin_config.ai_secret_key,
            base_url="https://api.atomecho.cn/v1",
        )
        self.plugin_config = plugin_config
        self.session = session

    async def get_session_message(self) -> list[MessageRecord]:
        """获取消息记录
        返回值:
        * ``List[MessageRecord]``: 消息记录列表
        """
        beijing_tz = zoneinfo.ZoneInfo("Asia/Shanghai")
        records = await get_message_records(
            session=self.session,
            id_type=SessionIdType.GROUP,
            time_start=datetime.now(beijing_tz).replace(hour=0),
            time_stop=datetime.now(beijing_tz).replace(hour=22),
        )
        return records

    async def get_ai_message_res(self, message: str) -> ChatCompletion:
        """异步获取AI回复消息的结果。

        参数:
        message (str): 需要AI进行响应的用户消息文本。

        返回值:
        ChatCompletion: AI生成的聊天回复内容。
        """
        content = "如下是一段多个用户参与的聊天记录，换行符'\n'代表一条消息的终结，请提取有意义的词句，总结这段聊天记录,字数在300字以内:" + message
        # content_list = await self.content_cutting(content)
        response = self.client.chat.completions.create(
            model="Llama3-Chinese-8B-Instruct",
            messages=[
                {"role": "user", "content": content}
            ],
            temperature=0.3,
            stream=False
        )
        return response

    async def load_filter_keywords(self) -> list:
        """加载过滤关键词
        `    返回值:
        * ``List[str]``: 过滤关键词列表
        """
        filepath = self.plugin_config.keywords_file_path
        with open(filepath, 'r', encoding='utf-8') as file:
            keywords = file.readlines()
        # 移除每个关键词末尾的换行符
        keywords = [keyword.strip() for keyword in keywords]
        return keywords

    async def filter(self, records: list) -> str:
        """过滤消息

        Parameters:
        - records: 待过滤消息

        Returns:
        - 已过滤消息,一坨str, 用换行符隔开
        """
        records_list = []
        keywords = await self.load_filter_keywords()
        for record in records:
            # 1.去除空消息 2.过滤指令"今日群聊" 3.去除机器人id
            if (record.plain_text != "" and
                int(record.session.id1) not in self.plugin_config.exclude_user_list and
                    all(keyword not in record.plain_text for keyword in keywords)):
                records_str = f"{record.plain_text}"
                records_list.append(records_str)
        records_merged = '\n'.join(records_list)
        return records_merged

    async def content_cutting(self, content: str, max_byte_size: int) -> list:
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
        records_merged_list = self._message_handle()
        total_length = sum(len(word.encode('utf-8'))
                           for word in records_merged_list)
        return total_length

    async def _message_handle(self) -> list:
        """处理消息,先过滤，然后再切割,获得切割后的消息list
        """
        record = await self.get_session_message()
        content_filter = await self.filter(record)
        content_cut = await self.content_cutting(content_filter, max_byte_size=3000)
        return content_cut
    async def generate_ai_message(self) -> str:
        """逐段生成ai总结，并计算token
        """
        records_merged_list = self._message_handle()
        for record in records_merged_list:
            response = await self.get_ai_message_res(record)
            ai_summary=response.choices[0].message.content
            ai_summarization=ai_summarization+"\n===分割===\n"+ai_summary
            used_token=response.usage
            used_tokens=used_tokens+str(used_token)
            print(f"Staging Completed!")
        return ai_summarization,used_tokens

