from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

class Summary:
    def __init__(self, plugin_config):
        self.client = OpenAI(
            api_key=plugin_config.ai_secret_key,
            base_url="https://api.atomecho.cn/v1",
        )
        self.plugin_config = plugin_config

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
            model="Atom-13B-Chat",
            messages=[
                {"role": "user", "content": content}
            ],
            temperature=0.3,
            stream=False
        )
        return response

    async def load_filter_keywords(self) -> list:
        filepath = self.plugin_config.keywords_file_path
        with open(filepath, 'r', encoding='utf-8') as file:
            keywords = file.readlines()
        # 移除每个关键词末尾的换行符
        keywords = [keyword.strip() for keyword in keywords]
        return keywords
    # 过滤用户

    async def filter(self, records: list) -> list:
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
