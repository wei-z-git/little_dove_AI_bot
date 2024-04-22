import json
from openai import OpenAI


class Summary:
    def __init__(self, plugin_config):
        self.client = OpenAI(
            api_key=plugin_config.ai_secret_key,
            base_url="https://api.atomecho.cn/v1",
        )
        self.plugin_config = plugin_config

    # async def content_cutting(self, content) -> list:
    #     '''
    #     将content以2000字符为单位, 分割为list
    #     '''
    #     max_byte_size = 2000
    #     num_chunks = (len(content.encode('utf-8')) // max_byte_size) + 1
    #     max_chunk_size = len(content) // num_chunks
    #     chunks_list = []
    #     for chunk_number in range(num_chunks):
    #         # 计算当前部分的起始和结束索引
    #         start_index = chunk_number * max_chunk_size
    #         end_index = (chunk_number + 1) * max_chunk_size
    #         # 切割请求内容为当前部分
    #         current_chunk = content[start_index:end_index]
    #         chunks_list.append(current_chunk)
    #     return chunks_list

    async def get_ai_message_res(self, message: str) -> str:
        content = "如下是一段多个用户参与的聊天记录，请提取有意义的词句，总结这段聊天记录, 不要分段,字数在300字以内:" + message
        completion = self.client.chat.completions.create(
            model="Atom-7B-Chat",
            messages=[
                {"role": "user", "content": content}
            ],
            temperature=0.3,
            stream=False
        )
        # 获取ai总结的结果
        completion = completion.choices[0].message.content
        return completion

    async def load_filter_keywords(self, filepath: str) -> list:
        with open(filepath, 'r', encoding='utf-8') as file:
            keywords = file.readlines()
        # 移除每个关键词末尾的换行符
        keywords = [keyword.strip() for keyword in keywords]
        return keywords
    # 过滤用户

    async def filter_user(self, records: list) -> list:
        records_list = []
        for record in records:
            # 1.去除空消息 2.过滤指令"今日群聊" 3.去除机器人id
            if (record.plain_text != "" and 
                record.session.id1 not in self.plugin_config.exclude_user_list and 
                all(keyword not in record.plain_text for keyword in self.load_filter_keywords())):
                records_str = f"{record.plain_text}"
                records_list.append(records_str)
        records_merged = '\n'.join(records_list)
        return records_merged
