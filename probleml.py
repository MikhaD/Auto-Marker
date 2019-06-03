#Calculate the combined, potentially overlapping area of coverage by a given number of WAPs
#Algorithm by reddit user flen_paris, modified by Mikha Davids
#https://www.reddit.com/r/dailyprogrammer/comments/23b1pr/4182014_challenge_158_hard_intersecting_rectangles/?sort=confidence
#10/05/2019

def thickness(list):
    active_rects = 0
    prev_y = 0
    thickness = 0
    for type, y in list:
        if active_rects > 0:
            thickness += y - prev_y
        active_rects += type
        prev_y = y
    return thickness

def insert(list, event): 
    y = event[1]
    for i in range(0, len(list)):
        if list[i][1] >= y:
            list.insert(i, event)
            return
    list.append(event)

def totalArea(rectangles):
    events = []
    #Create a list of "events"
    #An event occurs when a rectangle starts or ends when scanning from left to right
    for _ in range(rectangles) :
        data = [eval(i) for i in input().split()]
        x1 = data[0] - data[2]
        y1 = data[1] - data[2]
        x2 = data[0] + data[2]
        y2 = data[1] + data[2]
        events.append((1, x1, y1, y2))
        events.append((-1, x2, y1, y2))        
    #Sort events based on x coord
    events.sort(key=lambda x: x[1])

    #start sweep
    current_rectangles = [] #List of (1, y) and (-1, y) tuples, sorted in ascending y
    prev_x = 0    
    area = 0
    for event in events:
        type, x, y1, y2 = event
        area += (x-prev_x) * thickness(current_rectangles)
        if type == 1:            
            insert(current_rectangles, (1, y1))
            insert(current_rectangles, (-1, y2))
        elif type == -1:
            current_rectangles.remove((1, y1))
            current_rectangles.remove((-1, y2))
        prev_x = x
    return area

v_rectangles = int(input())
v_index = 1

while v_rectangles != 0 :
    print(v_index, '{0:.2f}'.format(totalArea(v_rectangles)))
    v_index += 1
    v_rectangles = int(input())
