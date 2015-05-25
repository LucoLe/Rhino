import rhinoscriptsyntax as rs
import Rhino as r
from scriptcontext import doc

def Input():
    point = [10,10]
    surface1 = rs.GetObjects("Select inner surfaces")
    surface2 = rs.GetObjects("Select outer surfaces")
    return surface1, surface2, point

def Difference(startPt, normal, scale, surface2):
    
    midPt = rs.VectorAdd(startPt, scale*normal)
    endPt = rs.PointClosestObject(midPt, surface2)[1]
    dist1 = rs.VectorLength(rs.VectorSubtract(startPt, midPt))
    dist2 = rs.VectorLength(rs.VectorSubtract(midPt, endPt))
    diff = dist2 - dist1
    return diff

def Domain(startPt, normal, scale, surface2, diff):
    
    while diff > 0:
        
        diff = Difference(startPt, normal, scale, surface2)
        scale += 100
    
    return [0, scale-100]

def Bisectoin(a, b, surface2):
    
    c = (a+b)/2.0
    
    while (b-a)/2.0 > tol:
        
        if Difference(startPt, normal, c, surface2) == 0:
            return c
        elif Difference(startPt, normal, a, surface2) * Difference(startPt, normal, c, surface2) < 0:
            b = c
        else:
            a = c
        
        c = (a+b)/2.0
    
    return c


if __name__=="__main__":
    input = Input()
    
    rs.EnableRedraw(False)
    for srf in input[0]:
        
        k = 1
        uDomain = rs.SurfaceDomain(srf, 0)[1] - rs.SurfaceDomain(srf, 0)[0]
        vDomain = rs.SurfaceDomain(srf, 1)[1] - rs.SurfaceDomain(srf, 1)[0]
        midPtArr = []
        
        for i in range(1,input[2][0]):
            for j in range(1,input[2][1]):
                a = rs.SurfaceDomain(srf, 0)[0] + (i * uDomain/input[2][0])
                b = rs.SurfaceDomain(srf, 1)[0] + (j * vDomain/input[2][1])
                startPt = rs.EvaluateSurface(srf,a, b)
                normal = rs.SurfaceCurvature(srf, [a,b])[1]*k
                scale = 0
                diff = Difference(startPt, normal, scale, input[1])
                tol = 0.1
                
                domain = Domain(startPt, normal, scale, input[1], diff)
                scale = Bisectoin(domain[0], domain[1], input[1])
                
                midPt = rs.VectorAdd(startPt, scale*normal)
                endPt = rs.PointClosestObject(midPt, input[1])[1]
                midPtArr.append(rs.AddPoint(midPt))
                rs.AddLine(startPt, midPt)
                rs.AddLine(midPt, endPt)
        
        rs.AddSrfPtGrid([input[2][0]-1, input[2][1]-1], midPtArr)
        
    rs.EnableRedraw(True)