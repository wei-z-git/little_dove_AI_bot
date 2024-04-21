import httpx
import json
from openai import OpenAI


class Summary:
    def __init__(self, ai_secret_key: str):
        self.client = OpenAI(
            api_key=ai_secret_key,
            base_url="https://api.atomecho.cn/v1",
        )
    # async def get_access_token(self) -> str:
    #     '''
    #     使用 AK, SK 生成鉴权签名(Access Token)
    #     :return: access_token, 或是None(如果错误)
    #     '''
    #     url = "https://aip.baidubce.com/oauth/2.0/token"
    #     params = {"grant_type": "client_credentials",
    #               "client_id": self.ai_api_key, "client_secret": self.ai_secret_key}
    #     access_token = str(httpx.post(
    #         url, params=params).json().get("access_token"))
    #     return access_token

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
        content = "如下是一段多个用户参与的聊天记录，换行符代表一条消息的终结，请忽略不文明的词句，提取有意义的词句并总结这段聊天记录:" + message
        content_list = await self.content_cutting(content)
        final_result = ""
        for content_chunk in content_list:
            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + await self.get_access_token()
            payload = {"messages": [
                {"role": "user", "content": content_chunk}
            ]}
            payload = json.dumps(payload)
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                response = httpx.post(url, headers=headers,
                                      data=payload, timeout=60).text
                result = json.loads(response).get('result')
            except httpx.TimeoutException:
                result = "请求超时"
            final_result += result
        return result
