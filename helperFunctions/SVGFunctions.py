import re
import numpy as np

# Some svg path elements have "transform" attributes which change the entire coordinates in some predefined way - most commonly a translation
# This function corrects those coordinates
class PathTransform:

    def __init__(self):

        self.transforms = {}

    def setTransform(self,transformString):

        # parse transform string

        transformString = re.split("\(",transformString)
        transform = transformString[0]

        values = re.sub("\)","",transformString[1])
        values = re.split(" ",values)
        for i,value in enumerate(values):
            values[i] = float(value)

        self.transforms.update({transform:values})

    def applyTransforms(self,data,type='coords'):

        for transform in self.transforms:
            if transform == 'translate' and type == 'coords':
                data[0],data[1] = self._translate(data[0],data[1])

        return data

    def _translate(self,x,y):

        xTrans,yTrans = self.transforms['translate']

        x += xTrans
        y += yTrans

        return x,y

# Converting arc parameters from an endpoint to endpoint translation to a centre & angle translation
def endpointToCentreParameters(x1,y1,x2,y2,angle,largeArc,sweep,rx,ry):

    midX = (x1-x2)*0.5
    midY = (y1-y2)*0.5;

    cosAngle = np.cos(angle);
    sinAngle = np.sin(angle);
    xp = cosAngle*midX + sinAngle*midY;
    yp = cosAngle*midY-sinAngle*midX;

    xp2 = xp*xp;
    yp2 = yp*yp;

    rx2 = rx*rx;
    ry2 = ry*ry

    s = (xp2/rx2)+(yp2/ry2)

    if s<=1.0:
        c = np.sqrt(max(0.0,((rx2*ry2)-(rx2*yp2)-(ry2*xp2))/((rx2*yp2)+ry2*xp2)))

        if largeArc == sweep:
            c = -c
    else:
        s2 = np.sqrt(s)
        rx *=s2
        ry *=s2
        c = 0

    cpx = ((rx * yp) / ry) * c
    cpy = ((-ry * xp) / rx) * c
    centreX = ((x1 + x2) * 0.5) + (cosAngle * cpx) - (sinAngle * cpy);
    centreY = ((y1 + y2) * 0.5) + (sinAngle * cpx) + (cosAngle * cpy);

    ux = (xp - cpx) / rx;
    uy = (yp - cpy) / ry;
    vx = (-xp - cpx) / rx;
    vy = (-yp - cpy) / ry;

    length = np.hypot(ux, uy);

    startAngle = np.arccos(np.clip(ux / length,-1.0, 1.0));

    if (uy < 0):
        startAngle = -startAngle;

    startAngle += np.pi/2;

    deltaAngle = np.arccos(np.clip((ux * vx) + (uy * vy),-1.0, 1.0)
                           / (length * np.hypot(vx, vy)));

    if ((ux * vy) - (uy * vx) < 0):
        deltaAngle = -deltaAngle;

    if (sweep):
        if (deltaAngle < 0):
            deltaAngle += np.pi*2;
    else:
        if (deltaAngle > 0):
            deltaAngle -= np.pi*2;

    deltaAngle = np.fmod(deltaAngle,np.pi*2)

    return centreX, centreY, startAngle, deltaAngle