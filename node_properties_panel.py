import bpy
from bpy.props import *

class NodePropertiesPanel(bpy.types.Panel):
    bl_idname = "an.node_properties_panel"
    bl_label = "Node and Socket Settings"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return hasattr(context.active_node, "isAnimationNode")

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self.node, "width", text = "Width")
        col.prop(self.node, "bl_width_max", text = "Max Width")

        # Inputs
        row = layout.row()
        rows = len(self.node.inputs)
        row.template_list("an_SocketUiList", "", self.node, "inputs", self.node, "activeInputIndex", rows = rows, maxrows = rows)
        col = row.column(align = True)
        props = col.operator("an.move_input", text = "", icon = "TRIA_UP").moveUp = True
        col.operator("an.move_input", text = "", icon = "TRIA_DOWN").moveUp = False

        # Outputs
        row = layout.row()
        rows = len(self.node.outputs)
        row.template_list("an_SocketUiList", "", self.node, "outputs", self.node, "activeOutputIndex", rows = rows, maxrows = rows)
        col = row.column(align = True)
        col.operator("an.move_output", text = "", icon = "TRIA_UP").moveUp = True
        col.operator("an.move_output", text = "", icon = "TRIA_DOWN").moveUp = False

        layout.separator()
        layout.label("Identifier: " + self.node.identifier)

    @property
    def node(self):
        return bpy.context.active_node


class SocketUiList(bpy.types.UIList):
    bl_idname = "an_SocketUiList"

    def draw_item(self, context, layout, node, socket, icon, activeData, activePropname):
        if socket.nameSettings.editable:
            layout.prop(socket, "customName", emboss = False, text = "")
        elif socket.isLinked or socket.is_output: layout.label(socket.getDisplayedName())
        else: layout.label(socket.toString())

        if socket.removeable:
            socket.callFunctionFromUI(layout, "remove", icon = "X", emboss = False)

        icon = "RESTRICT_VIEW_OFF" if socket.show else "RESTRICT_VIEW_ON"
        layout.prop(socket, "show", text = "", icon_only = True, icon = icon, emboss = False)


class MoveInputSocket(bpy.types.Operator):
    bl_idname = "an.move_input"
    bl_label = "Move Input"

    moveUp = BoolProperty()

    @classmethod
    def poll(cls, context):
        socket = getActiveSocket(isOutput = False)
        return getattr(socket, "moveable", False)

    def execute(self, context):
        return moveSocket(isOutput = False, moveUp = self.moveUp)

class MoveOutputSocket(bpy.types.Operator):
    bl_idname = "an.move_output"
    bl_label = "Move Output"

    moveUp = BoolProperty()

    @classmethod
    def poll(cls, context):
        socket = getActiveSocket(isOutput = True)
        return getattr(socket, "moveable", False)

    def execute(self, context):
        return moveSocket(isOutput = True, moveUp = self.moveUp)


def moveSocket(isOutput, moveUp):
    socket = getActiveSocket(isOutput)
    socket.moveSocket(moveUp)

    node = socket.node
    if isOutput: node.activeOutputIndex = list(node.outputs).index(socket)
    else: node.activeInputIndex = list(node.inputs).index(socket)
    return {"FINISHED"}

def getActiveSocket(isOutput):
    node = bpy.context.active_node
    if node is None: return
    if isOutput: return node.activeOutputSocket
    else: return node.activeInputSocket