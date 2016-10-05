from . poly_spline import PolySpline
from . bezier_spline import BezierSpline
from .. import FloatList, Vector3DList

def createSplinesFromBlenderObject(object):
    if object is None: return []
    if object.type != "CURVE": return []

    splines = []

    for bSpline in object.data.splines:
        spline = createSplineFromBlenderSpline(bSpline)
        if spline is not None:
            splines.append(spline)
    return splines

def createSplineFromBlenderSpline(bSpline):
    if bSpline.type == "BEZIER":
        return createBezierSpline(bSpline)
    elif bSpline.type == "POLY":
        return createPolySpline(bSpline)
    return None

def createBezierSpline(bSpline):
    amount = len(bSpline.bezier_points)
    points = Vector3DList(length = amount)
    leftHandles = Vector3DList(length = amount)
    rightHandles = Vector3DList(length = amount)

    bSpline.bezier_points.foreach_get("co", points.getMemoryView())
    bSpline.bezier_points.foreach_get("handle_left", leftHandles.getMemoryView())
    bSpline.bezier_points.foreach_get("handle_right", rightHandles.getMemoryView())

    spline = BezierSpline(points, leftHandles, rightHandles)
    spline.cyclic = bSpline.use_cyclic_u
    return spline

def createPolySpline(bSpline):
    pointArray = FloatList(length = 4 * len(bSpline.points))
    bSpline.points.foreach_get("co", pointArray.getMemoryView())
    del pointArray[3::4]
    splinePoints = Vector3DList.fromFloatList(pointArray)

    spline = PolySpline(splinePoints)
    spline.cyclic = bSpline.use_cyclic_u
    return spline