"""通用工具函数模块

Copyright (C) 2018 fly_lxl@foxmail.com
CreatedAt 2018-07-19
"""

import re

EMAIL_PATTERN = re.compile('^[0-9A-Za-z_]+@[0-9A-Za-z]+\.[0-9A-Za-z]+$')

def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    if EMAIL_PATTERN.match(email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))

def paging(data, limit, offset, total):
    """对数据列表添加分页信息"""
    return {
        'data': data,
        'page': {
            'limit': limit,
            'offset': offset,
            'total': total,
            'count': len(data)
        }
    }