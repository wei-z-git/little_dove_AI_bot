# 要发送的完整请求内容
full_request_content = ""

# 定义每个部分的最大字符数
max_byte_size = 2000

# 计算要切割的部分数量
num_chunks = (len(full_request_content.encode('utf-8'))  // max_byte_size) 
max_chunk_size=len(full_request_content) // num_chunks
print(len(full_request_content.encode()))
# 循环发送每个部分
for chunk_number in range(num_chunks):
    # 计算当前部分的起始和结束索引
    start_index = chunk_number * max_chunk_size
    end_index = (chunk_number + 1) * max_chunk_size
    
    # 切割请求内容为当前部分
    current_chunk = full_request_content[start_index:end_index]

    print(f"部分 {chunk_number + 1}")
    print(current_chunk)
    print(1)
    # 可以在这里添加适当的错误处理逻辑，例如检查响应状态码等

    # async def _generate_ai_message(self, content_cut_origin_record) -> str:
    #     """逐段生成ai总结，并计算token
    #     [TO BE REMOVED]
    #     """
    #     if len(content_cut_origin_record) > 1:
    #         ai_summarization = ""
    #         used_tokens = ""
    #         for record in content_cut_origin_record:
    #             response = await self.get_ai_message_res(record)
    #             ai_summary = response.choices[0].message.content
    #             ai_summarization = ai_summary+"\n===分割===\n"+ai_summarization
    #             used_token = response.usage
    #             used_tokens = used_tokens+str(used_token)
    #             print(f"Staging Completed!")
    #     else:
    #         response = await self.get_ai_message_res(content_cut_origin_record[0])
    #         ai_summary = response.choices[0].message.content
    #         ai_summarization = ai_summary
    #         used_token = response.usage
    #         used_tokens = str(used_token)
    #         print(f"Staging Completed!")
    #     return ai_summarization, used_tokens