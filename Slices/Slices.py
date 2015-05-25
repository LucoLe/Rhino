import rhinoscriptsyntax as rs

def Input():
    input = []
    input.append(rs.GetObject("Select volume element", 16))
    input.append(rs.GetObjects("Select cross section lines", 4))
    input.append(rs.GetReal("Input thickness", 1))
    return input

def CreateIntersections(input):
    intersections = []
    normals = []
    for i in input[1]:
        z = 100
        points = [(rs.CurveStartPoint(i)[0], rs.CurveStartPoint(i)[1], rs.CurveStartPoint(i)[2] - z), (rs.CurveStartPoint(i)[0], rs.CurveStartPoint(i)[1], rs.CurveStartPoint(i)[2] + z), (rs.CurveEndPoint(i)[0], rs.CurveEndPoint(i)[1], rs.CurveEndPoint(i)[2] + z), (rs.CurveEndPoint(i)[0], rs.CurveEndPoint(i)[1], rs.CurveEndPoint(i)[2] - z)]
        intersectionPlane = rs.AddSrfPt(points)
        intersection = rs.IntersectBreps(input[0], intersectionPlane)
        for i in intersection:
            intersections.append(i)
            normals.append(rs.CurveNormal(i))
        rs.DeleteObject(intersectionPlane)
    return intersections, normals

def CreateExtrusions(extrusionInput, input):
    for i in range(len(extrusionInput[0])):
        startPt = rs.PointAdd(rs.CurveStartPoint(extrusionInput[0][i]), rs.VectorScale(extrusionInput[1][i], -input[2]/2))
        endPt = rs.PointAdd(rs.CurveStartPoint(extrusionInput[0][i]), rs.VectorScale(extrusionInput[1][i], +input[2]/2))
        path = rs.AddLine(startPt, endPt)
        surface = rs.MoveObject(rs.AddPlanarSrf(extrusionInput[0][i]), rs.VectorScale(extrusionInput[1][i], -input[2]/2))
        rs.ExtrudeSurface(surface, path, endPt)
        rs.DeleteObjects([path, surface, extrusionInput[0][i]])
    return



if __name__=="__main__":
    input = Input()
    rs.EnableRedraw(False)
    extrusionInput = CreateIntersections(input)
    CreateExtrusions(extrusionInput, input)
    rs.HideObjects(input[0])
    rs.HideObjects(input[1])
    rs.EnableRedraw(True)