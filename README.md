# wecomreceiver

企业微信应用消息接收接口，作为[Flask.Blueprint](https://flask.palletsprojects.com/en/latest/tutorial/views/)使用。

由于可以注册多个监听器，且回复的要求比较严格，因此没有做回复，需使用[wecomsan](https://github.com/barryZZJ/wecomsan)异步回复。

## 用法参考

`pip install flask`
`pip instasll loguru`

```python
from WecomReceiver.WecomReceiver import WecomReceiver
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
def on_msg(
    content: str,
    toUserName: str,
    fromUserName: str,
    createTime: str,
    msgType: str,
    msgId: str,
    agentID: str,
    ):
    """
    收到消息时所有信息如上，可以只定义需要的形参。
    
    参考：
    https://developer.work.weixin.qq.com/document/10514
    https://developer.work.weixin.qq.com/document/path/90240
    
    :param content: 用户发送的消息,
    :param toUserName: 企业微信CorpID,
    :param fromUserName: 发送方成员UserID,
    :param createTime: 消息创建时间（整型）,
    :param msgType: 固定为'text',
    :param msgId: 消息对应的唯一id，可用于排重,
    :param agentID: 企业应用的id，整型,
    """
    # handle messages here
    pass


# 主app部分:
from flask import Flask
app = Flask(__name__)

# import bp之后注册到app上即可
app.register_blueprint(bp)

app.run(port=5000)
```