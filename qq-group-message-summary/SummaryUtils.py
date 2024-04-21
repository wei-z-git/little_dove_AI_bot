import json
from openai import OpenAI


class Summary:
    def __init__(self, ai_secret_key: str):
        self.client = OpenAI(
            api_key=ai_secret_key,
            base_url="https://api.atomecho.cn/v1",
        )

    async def content_cutting(self, content) -> list:
        '''
        将content以2000字符为单位, 分割为list
        '''
        max_byte_size = 2000
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

    async def get_ai_message_res(self, message: str) -> str:
        content = "如下是一段多个用户参与的聊天记录，请提取有意义的词句并总结这段聊天记录，可以根据内容主题不同分多个段落:" + message
        # content_list = await self.content_cutting(content)
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
