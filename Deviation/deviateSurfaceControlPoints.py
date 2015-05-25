import rhinoscriptsyntax as rs
from datetime import datetime

def Input():
    surface = rs.GetObjects("Select surfaces to deviate", 16)
    isoSurfaces = rs.GetObjects("Select isosurfaces", 16)
    borderSrfs = rs.GetObjects("Select border surfaces group")
    return [surface, isoSurfaces, borderSrfs]

def SortIsoSurfaces(arr):
    
    def getKey(item):
        return rs.ObjectName(item)
    arr.sort(key=getKey)
    return arr

def ExplodeIsoSurfaces(isoSurfaces):
    explodedIsoSurfaces = []
    for i in isoSurfaces:
        tempExplodedIsoSurfaces = rs.ExplodePolysurfaces(i)
        for j in tempExplodedIsoSurfaces:
            rs.ObjectName(j, rs.ObjectName(i))
        explodedIsoSurfaces += tempExplodedIsoSurfaces
    
    return explodedIsoSurfaces

def Deviation(point, dev1, dev2):
    
    srfcs1 = rs.ObjectsByName(dev1)
    point1 = rs.PointClosestObject(point, srfcs1)[1]
    
    srfcs2 = rs.ObjectsByName(dev2)
    point2 = rs.PointClosestObject(point, srfcs2)[1]
    
    dist1 = rs.Distance(point, point1)
    dist2 = rs.Distance(point, point2)
    
    dev1 = float(dev1)
    dev2 = float(dev2)
    
    dev = (dev1 + (((dev2 - dev1)*dist1)/(dist1 + dist2)))/100
    
    return dev

def PointsDeviate(inputSrfc, borderSrfs):
    
    rs.EnableObjectGrips(inputSrfc)
    nrPoints = rs.ObjectGripCount(inputSrfc)
    
    for i in range(0,nrPoints):
        oldPos = rs.ObjectGripLocation(inputSrfc, i)
        name = rs.ObjectName(rs.PointClosestObject(oldPos, borderSrfs)[0]).split("-")
        deviation = Deviation(oldPos, name[0], name[1])
        newPos = [oldPos[0], oldPos[1], oldPos[2] + deviation]
        rs.ObjectGripLocation(inputSrfc, i, newPos)


if __name__=="__main__":
    input = Input()
    
    isoSurfaces = SortIsoSurfaces(input[1])
    explodedIsoSurfaces = ExplodeIsoSurfaces(isoSurfaces)
    
    t1 = datetime.now()
    
    rs.EnableRedraw(False)
    for i in input[0]:
        PointsDeviate(i, input[2])
    
    rs.DeleteObjects(explodedIsoSurfaces)
    rs.EnableRedraw(True)
    
    t2 = datetime.now()
    timeDiff = t2 - t1
    print timeDiff