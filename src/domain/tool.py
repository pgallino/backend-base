from dataclasses import dataclass


@dataclass
class Tool:
    id: int
    name: str
    description: str

    @classmethod
    def from_input(cls, name: str, description: str) -> "Tool":
        return cls(id=0, name=name, description=description)


def build_tool(name: str, description: str) -> Tool:
    return Tool.from_input(name, description)
