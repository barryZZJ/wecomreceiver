import datetime
from pydantic import BaseModel, Field
from typing import Literal

# https://developer.work.weixin.qq.com/document/path/90239

MSGTYPE = Literal['text', 'image', 'voice', 'video', 'location', 'link']


class BaseMessage(BaseModel):
    agentID: int = Field(alias='AgentID')
    """企业应用的id，整型。可在应用的设置页面查看"""
    createTime: datetime.datetime = Field(alias='CreateTime')
    """消息创建时间（整型，秒级时间戳）"""
    fromUserName: str = Field(alias='FromUserName')
    """成员UserID，字母(+数字)"""
    msgType: MSGTYPE = Field(alias='MsgType')
    """消息类型"""
    msgId: int = Field(alias='MsgId')
    """消息id，64位整型"""
    toUserName: str = Field(alias='ToUserName')
    """企业微信CorpID，字母+数字"""


class TextMessage(BaseMessage):
    content: str = Field(alias='Content')
    """文本消息内容"""


# TODO
class ImageMessage(BaseMessage):
    # PicUrl	图片链接
    # MediaId	图片媒体文件id，可以调用获取媒体文件接口拉取，仅三天内有效
    ...


class VoiceMessage(BaseMessage):
    # MediaId	语音媒体文件id，可以调用获取媒体文件接口拉取数据，仅三天内有效
    # Format	语音格式，如amr，speex等
    ...


class VideoMessage(BaseMessage):
    # MediaId	视频媒体文件id，可以调用获取媒体文件接口拉取数据，仅三天内有效
    # ThumbMediaId	视频消息缩略图的媒体id，可以调用获取媒体文件接口拉取数据，仅三天内有效
    ...


class LocationMessage(BaseMessage):
    # Location_X	地理位置纬度
    # Location_Y	地理位置经度
    # Scale	地图缩放大小
    # Label	地理位置信息
    # AppType	app类型，在企业微信固定返回wxwork，在微信不返回该字段
    ...


class LinkMessage(BaseMessage):
    # Title	标题
    # Description	描述
    # Url	链接跳转的url
    # PicUrl	封面缩略图的url
    ...
