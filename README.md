# wecomreceiver

企业微信应用消息接收接口，作为[Flask.Blueprint](https://flask.palletsprojects.com/en/latest/tutorial/views/)使用。

由于可以注册多个监听器，且回复的要求比较严格，因此没有做回复，需使用[wecomsan](https://github.com/barryZZJ/wecomsan)异步回复。

## 用法参考

`pip install flask`
`pip instasll loguru`

```python
from WecomReceiver import WecomReceiver, BaseMessage, TextMessage, VideoMessage, LocationMessage, LinkMessage
from loguru import logger  # 可选

cid = ''  # 企业id
# 在企业的管理端后台，进入需要设置接收消息的目标应用，点击“接收消息”的“设置API接收”按钮，配置token和encodingAESKey。
token = ''
encodingAESKey = ''
blueprintname = 'subcribe_chan'

bp = WecomReceiver(
    token,
    encodingAESKey,
    cid,
    blueprintname,
    __name__,
    logger=logger,  # 如果不传入，默认会使用一个新的logger
    url_prefix='/subscribe_chan',
)

# 注册消息监听器
@bp.receive
def on_msg(msg: BaseMessage):
    """
    收到的消息类型、属性见message.py的注释
    
    参考：
    https://developer.work.weixin.qq.com/document/path/90239
    """
    # handle messages here
    if isinstance(msg, TextMessage):
        print(msg.content)


# 主app部分:
from flask import Flask
app = Flask(__name__)

# import bp之后注册到app上即可
app.register_blueprint(bp)

app.run(port=5000)
```