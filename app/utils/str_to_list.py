from typing import List


def str_to_int_list(s: str, sep: str = ",") -> List[int]:
    """
    把形如 "1,2,3" 的字符串转成 [1, 2, 3]
    空串或仅含空白时返回 []
    """
    if not s or not s.strip():
        return []
    return [int(item) for item in s.split(sep) if item.strip()]
