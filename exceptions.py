class InvalidParameter(Exception):
    """
        参数设置错误
    """


class NotFoundError(Exception):
    """
        没有找到内容
    """


class CreateError(Exception):
    """
        创建vertex或edge失败
    """


class RemoveError(Exception):
    """
        删除vertex或edge失败
    """


class UpdateError(Exception):
    """
    修改节点失败
    """


class DataFormatError(Exception):
    """
    输入数据格式错误
    """


class ServiceUnavailableException(Exception):
    """
    服务器过于繁忙不可用
    """