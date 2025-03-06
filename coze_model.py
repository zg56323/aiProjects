from pydantic import BaseModel, Field
from typing import List

# 定义 skill_category 到 shortcut command id 的映射
skill_to_command_id = {
    "权限管理": "7476028249949831209",
    "回答物理问题": "未明确映射",
    "提供学习建议": "未明确映射",
    "总结物理知识": "未明确映射",
    "针对知识点出题": "7475982490701037607",
    "批改学生答案并梳理知识点": "未明确映射",
    "笔记管理 - 记笔记": "7475982490700939303",
    "笔记管理 - 查笔记": "7475982490701004839",
    "笔记管理 - 删除笔记": "7475982490700972071",
    "知识图谱": "未明确映射",
    "论文查询": "未明确映射",
    "答疑": "7477087919560507392"
}

class CozeAgentOutput(BaseModel):
    generated_texts: List[str] = Field(
        default_factory=list,
        description="智能体生成的多条文本内容"
    )
    summary: str = Field(
        default="",
        description="对生成文本的简要总结"
    )
    commandId: str = Field(
        default="",
        description="快捷命令的ID，映射关系如下："
                    "权限管理 -> 7476028249949831209；"
                    "针对知识点出题 -> 7475982490701037607；"
                    "笔记管理 - 记笔记 -> 7475982490700939303；"
                    "笔记管理 - 查笔记 -> 7475982490701004839；"
                    "笔记管理 - 删除笔记 -> 7475982490700972071；"
                    "答疑 -> 7477087919560507392；其他技能未明确映射，显示'未明确映射'"
    )

    model_config = {
        "from_attributes": True
    }