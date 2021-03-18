
def draw_Dot36():#(self, painter):

    Arrayyy = [False, False, False, False, True, False, False, False]
    x_white = 70
    x_black = 75
    white_y = 20
    black_y = 12
    
    if Arrayyy[0] == True:
        x = x_white
        y = white_y
        print(x, y)
    elif Arrayyy[1] == True: 
        x = x_black + 20
        y = black_y
        print(x, y)
    elif Arrayyy[2] == True:
        x = x_white + 20
        y = white_y
        print(x, y)
    elif Arrayyy[3] == True: 
        x = x_black + 40
        y = black_y
    else: 
        x = 100
        y = 200
    print('FINAL')
    print(x)
    print(y)
    
draw_Dot36()


'''
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))


        # drawing white keys
        x = 70
        for rect in range(52):
            painter.drawRect(x, 200, 20, 170)
            x = x + 20
            #print(x)
        
        # drawing black keys
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        #first black key
        test = painter.drawRect(84, 200, 12, 110)
        test





  # drawing dots on white keys
        x = 75
        for rect in range(52):
            painter.drawEllipse(x, 350, 10, 10)
            x = x + 20
            print(x)
        
        # drawing dots on black keys
        #first black key
        painter.drawEllipse(86, 300, 8, 8)
        # following 7 octaves of black keys
        x = 126 # 6 breit
        for rect in range(7):
            painter.drawEllipse(x, 300, 8, 8)
            painter.drawEllipse(x+20, 300, 8, 8)
            painter.drawEllipse(x+60, 300, 8, 8)
            painter.drawEllipse(x+80, 300, 8, 8)
            painter.drawEllipse(x+100, 300, 8, 8)
            x = x + 140      

'''

