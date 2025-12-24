from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class MenuOut(BaseModel):
    id: int
    parent_id: int
    name: str
    path: Optional[str]
    component: Optional[str]
    redirect: Optional[str]
    icon: Optional[str]
    title: str
    hidden: bool = False
    keep_alive: bool = True
    always_show: bool = False
    params: Optional[dict] = None
    children: List["MenuOut"] = []

    class Config:
        orm_mode = True
        from_attributes = True


# 结构化路由列表
def flat_to_tree(items: List[Dict[str, Any]],
                 id_key: str = "id",
                 pid_key: str = "parent_id",
                 children_key: str = "children") -> List[Dict[str, Any]]:
    """
    扁平数据 → 树形结构，并把部分字段封装进 meta
    该函数将扁平化的列表数据转换为树形结构，并将部分特定字段封装到 meta 对象中。
    参数:
        items: 扁平化的数据列表，每个元素是一个字典
        id_key: 用作唯一标识符的字段名，默认为 "id"
        pid_key: 用作父节点标识的字段名，默认为 "parent_id"
        children_key: 用于存储子节点的字段名，默认为 "children"
    返回:
        转换后的树形结构数据列表
    """
    # 1. 建立 id -> node 的映射，并初始化 children
    # 创建一个字典，用于快速查找节点
    mapping: Dict[int, Dict[str, Any]] = {}
    for node in items:
        node_copy = node.copy()  # 避免污染原始数据
        node_copy[children_key] = []

        # 2. 抽字段进 meta
        meta_fields = ["title", "icon", "hidden", "always_show", "params"]
        meta = {k: node_copy.pop(k) for k in meta_fields if k in node_copy}
        # 统一把 hidden / always_show 转成 bool
        meta["hidden"] = bool(meta.get("hidden", False))
        meta["alwaysShow"] = bool(meta.pop("always_show", False))
        node_copy["meta"] = meta

        mapping[node_copy[id_key]] = node_copy

    # 3. 挂到父节点
    tree: List[Dict[str, Any]] = []
    for node in mapping.values():
        pid = node[pid_key]
        if pid == 0:
            tree.append(node)
        else:
            parent = mapping.get(pid)
            if parent:
                parent[children_key].append(node)

    return tree
