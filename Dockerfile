FROM registry.cn-hangzhou.aliyuncs.com/wei-z-git/nonebot2-base-image:latest


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 


COPY ./ /app/

CMD ["python3", "bot.py"]
