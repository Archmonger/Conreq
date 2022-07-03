from idom.core.types import ComponentType, VdomDict, _OwnType


class ConditionalRender:
    def __init__(self, element: ComponentType, should_render: bool) -> None:
        self.key = None
        self.type = self.__class__
        self.element = element
        self.render_flag = should_render

    def render(self) -> VdomDict | ComponentType | None:
        return self.element

    def should_render(self, new_object: _OwnType) -> bool:
        return new_object.render_flag
