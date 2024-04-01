"""
utils
"""


def order_member_by_time(data: str):
    """
        查询群员信息并按last_sent_time排序
    """
    try:

        vip_lists = read_accounts_from_file()
        # Only keep fields:user_id, sex, nickname, last_sent_time, join_time
        new_data = [{'user_id': d['user_id'], 'sex': d['sex'], 'nickname': d['nickname'],
                     'last_sent_time': d['last_sent_time'], 'join_time': d['join_time']} for d in data]
        # Ladies should not be including
        filtered_data = [item for item in new_data if item['sex'] != 'female']
        # Exclude accounts from the file
        filtered_data = [
            item for item in filtered_data if item['user_id'] not in vip_lists]
        # Ordered by last_sent_time
        json_data_sorted = sorted(
            filtered_data, key=lambda x: x['last_sent_time'])
        # Return top 10 items
        final_data = json_data_sorted[:10]

        return final_data
    except KeyError:
        return []


def read_accounts_from_file() -> str:
    """
    从文件中读取每一行账号信息
    """
    try:
        with open("qq-group-admin-plugin/configs/vip_list.txt", 'r', encoding='utf-8') as file:
            accounts =  [int(line.strip()) for line in file.readlines()]
        return accounts
    except FileNotFoundError:
        print(f"File not found:")
        return []

def order_member_by_time_dsa(data: str):
    """查询成员按最后一次发言时间排序
    """
    try:

        vip_lists = read_accounts_from_file()
        # Only keep fields:user_id, sex, nickname, last_sent_time, join_time
        new_data = [{'user_id': d['user_id'], 'sex': d['sex'], 'nickname': d['nickname'],
                     'last_sent_time': d['last_sent_time'], 'join_time': d['join_time']} for d in data]
        # Exclude accounts from the file
        filtered_data = [
            item for item in new_data if item['user_id'] not in vip_lists]
        # Ordered by last_sent_time
        json_data_sorted = sorted(
            filtered_data, key=lambda x: x['last_sent_time'])
        # Return bottom 10 items
        final_data = json_data_sorted[-10:]

        return final_data
    except KeyError:
        return []