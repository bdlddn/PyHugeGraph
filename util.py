import logging, re
from .exceptions import ServiceUnavailableException
import json
# from configparser import ConfigParser


def log(config):
    # config = ConfigParser()
    # config.read(config_file)
    # 创建logger，如果参数为空则返回root logger
    logger = logging.getLogger(config["logger"]["name"])
    if config["logger"]["level"] == "DEBUG":
        logger.setLevel(logging.DEBUG)  # 设置logger日志等级
    elif config["logger"]["level"] == "INFO":
        logger.setLevel(logging.INFO)
    elif config["logger"]["level"] == "WARNING":
        logger.setLevel(logging.WARNING)
    elif config["logger"]["level"] == "ERROR":
        logger.setLevel(logging.ERROR)
    elif config["logger"]["level"] == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)
    # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        # 创建handler
        log_file = config["logger"]["file"]
        # log_file = config["logger"]["file"] if os.path.exists(config["logger"]["file"]) else config["logger"]["file2"]
        fh = logging.FileHandler(log_file, encoding=config["logger"]["encoding"])
        ch = logging.StreamHandler()
        # 设置输出日志格式
        formatter = logging.Formatter(
            # fmt="%(asctime)s %(name)s %(filename)s %(message)s",
            fmt="[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s",
            datefmt="%Y/%m/%d %X"
            )
        # 为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 为logger添加的日志处理器
        logger.addHandler(fh)
        logger.addHandler(ch)
        # 直接返回logger
        return logger


def clean_logger_handlers(config):
    logger = logging.getLogger(config["logger"]["name"])
    if logger.handlers:
        logger.handlers = []


def read_csv_content(file_path, has_head=True):
    with open(file_path, encoding='utf-8') as fp:
        if has_head:
            fp.readline()
        for line in fp:
            yield line.rstrip("\n")
    yield "File End"


def read_csv_head(file_path, keys):
    with open(file_path, encoding='utf-8') as fp:
        key_dic = dict()
        raw_head = fp.readline().strip()
        head = raw_head.split("\t")
        for i, item in enumerate(head):
            if item in keys:
                key_dic[item] = i
        return raw_head, key_dic


def read_csv_file(file_path, keys, n, start_line, has_head=True):
    with open(file_path, encoding='utf-8') as fp:
        key_dic = dict()
        raw_head = fp.readline().strip()
        head = raw_head.split("\t")
        for i, item in enumerate(head):
            if item in keys:
                key_dic[item] = i
        data = []
        for i, line in enumerate(fp):
            if i < start_line:
                continue
            try:
                tmp = {"raw_line": line.rstrip("\n")}
                line = line.rstrip("\n").split("\t")
                dic = dict()
                for key in key_dic.keys():
                    dic[key] = line[key_dic[key]] if line[key_dic[key]] else 'null'
                tmp['dic'] = dic
                tmp['is_duty'] = False
                data.append(tmp)
            except Exception as e:
                print('Error line: {}'.format(tmp['raw_line']))
            if len(data) == n:
                yield data
                data = []
        yield data


def read_txt_file(file_path, keys, n, start_line, has_head=False):
    with open(file_path, encoding='utf-8') as fp:
        data = []
        for i, line in enumerate(fp):
            if i < start_line:
                continue
            try:
                tmp = {"raw_line": line.rstrip("\n")}
                line = line.rstrip("\n").split("\t")
                dic = dict()
                for j, key in enumerate(keys):
                    dic[key] = line[j] if line[j].rstrip() else 'null'
                tmp['dic'] = dic
                tmp['is_duty'] = False
                data.append(tmp)
            except Exception as e:
                print("Error line: {}".format(tmp['raw_line']))
                pass
            if len(data) == n:
                yield data
                data = []
        yield data


def read_csv_file2(file_path, keys, n, start_line, has_head=True):
    with open(file_path, encoding='utf-8') as fp:
        key_dic = dict()
        raw_head = fp.readline().strip()
        head = raw_head.split("\t")
        for i, item in enumerate(head):
            if item.startswith('"'):
                item = item[1:]
            if item.endswith('"'):
                item = item[:-1]
            if item in keys:
                key_dic[item] = i
        data = []
        for i, line in enumerate(fp):
            if i < start_line:
                continue
            try:
                tmp = {"raw_line": line.rstrip("\n")}
                line = line.rstrip("\n").split("\t")
                dic = dict()
                for key in key_dic.keys():
                    item = line[key_dic[key]]
                    if item.startswith('"'):
                        item = item[1:]
                    if item.endswith('"'):
                        item = item[:-1]
                    dic[key] = item
                tmp['dic'] = dic
                tmp['is_duty'] = False
                data.append(tmp)
            except Exception as e:
                print('Error line: {}'.format(tmp['raw_line']))
            if len(data) == n:
                yield data
                data = []
        yield data


def check_data_format(data, check_dic):
    for key in check_dic.keys():
        if key in data:
            if check_dic[key] == "not_null":
                if data[key].strip() == '' or data[key].strip() == 'null':
                    return False
            elif check_dic[key] == "is_ip":
                if not is_ip(data[key]):
                    return False
            elif check_dic[key] == "not_ip":
                if data[key].strip() == '' or data[key].strip() == 'null':
                    return False
                elif is_ip(data[key]):
                    return False
    return True


def is_ip(line):
    line = line.strip()
    res = re.match("^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$", line)
    if res:
        return True
    return False


def create_exception(reponse_content):
    data = json.loads(reponse_content)
    if "ServiceUnavailableException" in data["exception"]:
        raise ServiceUnavailableException('ServiceUnavailableException, "message": "{}", "cause": "{}"'.
                                           format(data["message"], data["cause"]))
    else:
        raise Exception(reponse_content)


def short_string(s, length=120):
    if len(s) > length:
        return s[:length] + '...'
    elif s == '':
        return 'null'
    else:
        return s


def format_time_str(s):
    res = re.match('^\d{4}-\d{2}-\d{2}$', s)
    if res:
        return '{} 00:00:00'.format(s)
    res = re.match('^\d{8}$', s)
    if res:
        return '{}-{}-{} 00:00:00'.format(s[:4], s[4:6], s[6:8])
    return None
