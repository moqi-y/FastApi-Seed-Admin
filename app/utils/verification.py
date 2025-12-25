import re

"""
验证工具
"""


def check_email(email: str):
    """
    验证邮箱
    :param email: 邮箱地址
    :return: bool
    """
    if not email:
        return False
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return False
    return True


def check_phone(phone: str):
    """
    验证手机号
    :param phone: 手机号
    :return: bool
    """
    if not phone:
        return False
    if not re.match(r"^1[3-9]\d{9}$", phone):
        return False
    return True


def check_fixed_phone(phone: str):
    """
    验证固定电话
    :param phone: 固定电话
    :return: bool
    """
    if not phone:
        return False
    if not re.match(r"^(0\d{2,3}-?)?\d{7,8}$", phone):
        return False
    return True


def check_pass_card(card_number: str):
    """
    验证身份证
    :param card_number: 身份证号码
    :return: bool
    """
    if not card_number:
        return False
    if not re.match(r"^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[0-9X]$", card_number):
        return False
    return True
