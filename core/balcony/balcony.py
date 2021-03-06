import bmesh

from .balcony_types import create_balcony
from ...utils import get_edit_mesh, FaceMap, add_facemap_for_groups


class Balcony:
    @classmethod
    def build(cls, context, prop):
        me = get_edit_mesh()
        bm = bmesh.from_edit_mesh(me)
        faces = [face for face in bm.faces if face.select]

        if cls.validate(faces):
            cls.add_balcony_facemaps()
            create_balcony(bm, faces, prop)
            bmesh.update_edit_mesh(me, True)
            return {"FINISHED"}
        return {"CANCELLED"}

    @classmethod
    def add_balcony_facemaps(cls):
        groups = FaceMap.BALCONY
        add_facemap_for_groups(groups)

    @classmethod
    def validate(cls, faces):
        if faces:
            # -- ensure none are upward facing
            if not any([round(f.normal.z, 1) for f in faces]):
                return True
        return False
