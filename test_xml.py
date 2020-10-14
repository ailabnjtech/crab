import xml.dom.minidom
import math


fp = r'crabs_old.xml'

doc = xml.dom.minidom.parse(fp)
collection = doc.documentElement


class Point:
    def __init__(self, p):
        self.x = int(p.getAttribute('x'))
        self.y = int(p.getAttribute('y'))


def angle(p1, p2, p3, p4):
    dx1 = p1.x - p2.x
    dy1 = p1.y - p2.y
    dx2 = p3.x - p4.x
    dy2 = p3.y - p4.y
    angle1 = math.atan2(dy1, dx1)
    angle1 = float(angle1 * 180/math.pi)
    angle2 = math.atan2(dy2, dx2)
    angle2 = float(angle2 * 180/math.pi)
    if angle1*angle2 >= 0:
        included_angle = abs(angle1-angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
    if included_angle > 180:
        included_angle = 360 - included_angle
    return included_angle


def length(p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)


def get_dis(p, lp1, lp2):
    a = lp2.y - lp1.y
    b = lp1.x - lp2.x
    c = lp2.x*lp1.y - lp1.x*lp2.y
    return (math.fabs(a*p.x + b*p.y+c))/(math.pow(a*a+b*b, 0.5))


p_names = ('l1', 'l4', 'l5', 'l8', 'r1', 'r4', 'r5', 'r8', 'c8', 'c9', 'd3', 'd8', 'd1', 'd5', 'd6', 'd10')
p_cnt = len(p_names)
with open('testxml-ds.csv', 'wb') as fn:
    for image in collection.getElementsByTagName("image"):

        for box in image.childNodes:
            if isinstance(box, xml.dom.minidom.Text):
                continue
            parts = {}
            results = []
            for part in box.childNodes:
                if isinstance(part, xml.dom.minidom.Text):
                    continue
                if part.getAttribute('name') not in p_names:
                    continue
                parts[part.getAttribute('name')] = Point(part)
            if len(parts) != p_cnt:
                continue
            # 计算线段比例
            line_7_8 = length(parts['c8'], parts['c9'])                                  # 中部基准线段长度
            results.append(length(parts['l8'], parts['r1'])/line_7_8)                   # 顶部角线段长度
            results.append(length(parts['l4'], parts['r5'])/line_7_8)                   # 第二角线段长度
            results.append(length(parts['l1'], parts['l4'])/line_7_8)                   # 左第二边线段长度
            results.append(length(parts['l5'], parts['l8'])/line_7_8)                   # 左第一边线段长度
            results.append(length(parts['r1'], parts['r4'])/line_7_8)                   # 右第一边线段长度
            results.append(length(parts['r5'], parts['r8'])/line_7_8)                   # 右第二边线段长度
            results.append(length(parts['d3'], parts['d8'])/line_7_8)                   # 底部线段长度
            results.append(get_dis(parts['l5'], parts['l1'], parts['l4'])/line_7_8)     # 左第一凹到左第二线距离
            results.append(get_dis(parts['l5'], parts['l8'], parts['c8'])/line_7_8)     # 左第一凹到左顶角与中左点距离
            results.append(get_dis(parts['r4'], parts['r5'], parts['r8'])/line_7_8)     # 右第一凹到右第二线距离
            results.append(get_dis(parts['r4'], parts['r1'], parts['c9'])/line_7_8)     # 右第一凹到右顶角与中右点距离
            results.append(get_dis(parts['c8'], parts['l8'], parts['r1'])/line_7_8)     # 中左点到顶部角线段距离
            results.append(get_dis(parts['c8'], parts['d3'], parts['d8'])/line_7_8)     # 中左点到底部线段距离
            results.append(get_dis(parts['c9'], parts['l8'], parts['r1'])/line_7_8)     # 中右点到顶部角线段距离
            results.append(get_dis(parts['c9'], parts['d3'], parts['d8'])/line_7_8)     # 中右点到底部线段距离

            # 计算点角度
            results.append(angle(parts['l1'], parts['l4'], parts['l5'], parts['l8']))       # 左一边与左二边夹角
            results.append(angle(parts['r1'], parts['r4'], parts['r5'], parts['r8']))       # 右一边与右二边夹角
            results.append(angle(parts['r1'], parts['r4'], parts['l5'], parts['l8']))       # 左一边与右一边夹角
            results.append(angle(parts['l1'], parts['l4'], parts['c8'], parts['c9']))       # 左二边与中线夹角
            results.append(angle(parts['r5'], parts['r8'], parts['c8'], parts['c9']))       # 右二边与中线夹角
            results.append(angle(parts['d3'], parts['d8'], parts['c8'], parts['c9']))       # 底边与中线夹角
            results.append(angle(parts['d3'], parts['d8'], parts['d3'], parts['c8']))       # 底边与中左点夹角
            results.append(angle(parts['d3'], parts['d8'], parts['d8'], parts['c9']))       # 底边与中右点夹角
            results.append(angle(parts['l4'], parts['c8'], parts['c8'], parts['l8']))       # 左侧角点与中左点夹角
            results.append(angle(parts['r1'], parts['c9'], parts['c9'], parts['r5']))       # 右侧角点与中右点夹角
            results.append(angle(parts['d1'], parts['d3'], parts['d3'], parts['c8']))       # 左底斜边与中左点夹角
            results.append(angle(parts['d1'], parts['d3'], parts['d3'], parts['d5']))       # 左底斜边与左底边夹角
            results.append(angle(parts['d6'], parts['d8'], parts['d8'], parts['c9']))       # 右底斜边与中右点夹角
            results.append(angle(parts['d6'], parts['d8'], parts['d8'], parts['d10']))      # 右底斜边与右底边夹角

            fn.write("{}, {}\n".format(image.getAttribute('file'), ", ".join([str(i) for i in results])).encode())
            print(image.getAttribute('file'))



