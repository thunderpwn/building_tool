import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, PointerProperty

from ..railing import RailProperty
from ..generic import SizeOffsetProperty


class BalconyProperty(bpy.types.PropertyGroup):
    redo: BoolProperty()

    width: FloatProperty(
        name="Balcony Width",
        min=0.01,
        max=100.0,
        default=1.2,
        description="Width of balcony",
    )

    open_items = [
        ("NONE", "None", "", 0),
        ("FRONT", "Front", "", 1),
        ("LEFT", "Left", "", 2),
        ("RIGHT", "Right", "", 3),
    ]

    open_side: EnumProperty(
        name="Open Side",
        items=open_items,
        default="NONE",
        description="Sides of the balcony with no railing",
    )

    has_railing: BoolProperty(
        name="Add Railing", default=True, description="Whether the balcony has railing"
    )
    rail: PointerProperty(type=RailProperty)
    size_offset: PointerProperty(type=SizeOffsetProperty)

    def init(self, wall_dimensions):
        self['wall_dimensions'] = wall_dimensions
        self.size_offset.init((self['wall_dimensions'][0], self['wall_dimensions'][1]), default_size=(1.0, 0.2), default_offset=(0.0, 0.0))

    def draw(self, context, layout):
        self.size_offset.draw(context, layout)

        row = layout.row()
        row.prop(self, "width")

        layout.prop(self, "has_railing", toggle=True)
        if self.has_railing:
            box = layout.box()
            box.prop_menu_enum(self, "open_side", text="Open")
            self.rail.draw(context, box)
