FROM registry.jihulab.com/nonebot2-wei-z/nonebot2-base-image:0.0.1


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 


COPY ./ /app/

CMD ["python3", "bot.py"]
