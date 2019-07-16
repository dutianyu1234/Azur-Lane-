import time,random,tkinter,datetime
import numpy as np
import matplotlib.pyplot as pltimport
import pyautogui as pag

from PIL import ImageGrab,Image
from tkinter import messagebox
from scipy import signal

from pymouse import PyMouse
m=PyMouse()
top = tkinter.Tk()
pic_path = 'c:/Users/柏木英理/Desktop/程序集/Python/MyClickScripts/'

resolution = (1366/1920,766/1080)

# 定义各个功能所需截取的图片

# 关卡界面的立即前往功能
pic1 = (1207,657,1490,752)
path1 = pic_path + 'pic1.jpg'
#出击准备界面的立即前往功能
pic2 = (1410,858,1669,947)
path2 = pic_path + 'pic2.jpg'

#规避按钮
pic3 = (1144,507,1476,617)
path3 = pic_path + 'pic3.jpg'

#出击按钮
pic4 = (1319,839,1737,998)
path4 = pic_path + 'pic4.jpg'

#清空潜艇编队
pic5 = (1630,741)
path5 = pic_path + 'pic5.jpg'

#自动清理船舱
pic6 = (593,676,871,772)
path6 = pic_path + 'pic6.jpg'
self_clean_position = {0:(223,845),1:(438,850),2:(674,835),3:(915,849)}
next_action = {0:(1596,957),1:(1441,898),2:(669,829),3:(1479,872),4:(1104,731),5:(953,886),6:(117,74)}


#关卡信息
#1-4
pic_104 = (1,1,1,1)
position_104 = (1144,275)
path_104 =  pic_path + 'pc1.4.jpg'
loop_104 =[(743,480),(724,595),(897,719),(1268,721)]
number_to_boss_104 = 1
boss_position_104 = {1:(1469,727)}
#3-4吃喝
pic_304 = (841,471,973,608)
position_304 = (900,550)
path_304 = pic_path + 'pic3.4.jpg'
loop_304 = [(1429,851),(904,877),(501,884),(536,612),(712,733),(904,604),(897,474),(1086,735),(1293,738)]
number_to_boss_304 = 3
boss_position_304 ={1:(1647,721),2:(1652,849)}

#峡湾间的星辰sp3
pic_xiawan_sp3 = (1221,667,1364,804)
path_xiawan_sp3 = pic_path + 'pic_xiawan_sp3.jpg'


#识别图像并点击，成功返回真，失败返回假
def image_distinguish(position,path):
    #读取预备图像
    img = np.array(Image.open(path).convert('L'))
    #确定需要截取的图像位置
    grab_size = position

    #开始截屏
    time.sleep(3)
    img2 = np.array(ImageGrab.grab(grab_size).convert('L'))

    #计算相似度并确认是否点击
    temp = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
                s = abs(int(img[i][j])-int(img2[i][j]))
                temp = temp + s*s
    temp = temp/len(img)/len(img[0])
    print(temp)
    if temp<400 :
        m.click(int((position[0]+position[2])/2),int((position[1]+position[3])/2))
        return True
    else:
        return False

#检测船刷新位置
def det_position(typeofship):
    global img
    ame = np.array(ImageGrab.grab().convert('L'))
    ame = (ame-np.mean(ame))/np.std(ame)

    if (typeofship == 1):#普通船
        img = np.array(Image.open(pic_path + 'm15.png').convert('L'))
    else:
        if (typeofship == 2):#航空船
            img = np.array(Image.open(pic_path + 'm23.png').convert('L'))
        else:
            if (typeofship == 3):#主力船
                img = np.array(Image.open(pic_path + 'm33.png').convert('L'))
            else:
                if (typeofship == 4):#宝箱船
                     img = np.array(Image.open(pic_path + 'm33.png').convert('L'))
                else:
                    if (typeofship == 5):#boss船
                        img = np.array(Image.open(pic_path + 'm53.png').convert('L'))

    if (typeofship == 6):
        img = np.array(Image.open(pic_path + 'sure.png').convert('L'))
    if (typeofship == 7):
        img = np.array(Image.open(pic_path + 'victory.png').convert('L'))
        
    img = (img - np.mean(img))/np.std(img)
    img = np.rot90(img,k=2)

    res = signal.fftconvolve(ame,img,mode = 'same')

    if (len(res)==0):
        print("false")
        return [0,0,False]
    posx,posy = divmod(np.argmax(res),res.shape[1])
    h,w = img.shape

    h2 = int(h/2)
    w2 = int(w/2)
    
    if (posx<h2 or posy<w2):
        print("false")
        return [0,0,False]
    t1 = ame[(posx-h2):(posx+h2),(posy-w2):(posy+w2)]

    image = Image.fromarray(t1)
    #image.save('d:/test.jpg')

    return [int(posy),int(posx),True]



#如果船舱已满，自动清理船舱
def self_dec_full():
    if image_distinguish(pic6,path6):
        time.sleep(2+random.random())
        for s in range(len(self_clean_position)):
            m.click(self_clean_position[s][0],self_clean_position[s][1])
            time.sleep(2+random.random())
        for c in range(len(next_action)):
            m.click(next_action[c][0],next_action[c][1])
            time.sleep(2+random.random())
        time.sleep(5+random.random()*2)
        print("ready")
        return True
    else:
        return False
    

#存储图片，初始化使用
def save_picture(position,path):
    clip = ImageGrab.grab(position)
    if (clip != None):
        clip.save(path,quality = 95,subsampling = 0)

#选择关卡后提示信息
def helloCallBack():
   messagebox.showinfo( "提示", "关卡选择成功！")

#选择关卡3-4
def setinfo_304():
    global number_to_boss,pic,position,path,loop,boss_position
##    helloCallBack()
    number_to_boss = number_to_boss_304         
    position = position_304                            
    loop = loop_304                             
    boss_position = boss_position_304
    top.destroy()

#选择关卡1-4
def setinfo_104():
    global a,number_to_boss,pic,position,path,loop,boss_position
##    helloCallBack()
    number_to_boss = number_to_boss_104         
    position = position_104                            
    loop = loop_104                             
    boss_position = boss_position_104
    top.destroy()

##pic10=(604,294,741,361)
##path10 =pic_path + 'pic10.png'
Level_save = tkinter.Button(top, text ="Do you want to save picture?", command = lambda :save_picture(pic10,path10),height = 10,width = 10)
Level_save.pack()
Level_304 = tkinter.Button(top, text ="3-4", command = setinfo_304,height = 10,width = 10)
Level_304.pack()
Level_104 = tkinter.Button(top, text ="1-4", command = setinfo_104,height = 10,width = 10)
Level_104.pack()
top.mainloop()

number_to_boss = 5
s = 0
c = 0


while True:
    m.click(1000*resolution,600*resolution)


    if image_distinguish(pic1,path1):
        time.sleep(2+random.random()*2)
        if (self_dec_full()):
            m.click(700*resolution,300*resolution)
            time.sleep(2+random.random()*2)

        m.click(1630*resolution,500*resolution)
        
        m.click(1350,700)
        time.sleep(2+random.random()*2)
        m.click(1630,741)
        time.sleep(1+random.random())
        m.click(1520,900)
        time.sleep(10+random.random()*3)
        m.move(960,540)
        pag.dragTo(860,440,2)

    for i in range(4):
##        if (det_position(6)[2]):
##            m.click(det_position(6)[0],det_position(6)[1])
        
        if det_position(i+1)[2] and s<number_to_boss:
            t = det_position(np.mod(i,3)+1)
            m.click(t[0],t[1])

            time.sleep(5+random.random()*3)
            if image_distinguish(pic3,path3):#如果有遇敌，再次点击
                time.sleep(5+random.random()*3)
                m.click(t[0],t[1])
            if image_distinguish(pic4,path4):
                if (self_dec_full()):
                    image_distinguish(pic4,path4)

##                while (not det_position(7)[2]):
##                     pass
##                m.click(det_position(7)[0],det_position(7)[1]+400)
                time.sleep(50+random.random()*5)
                m.click(240,850)
                time.sleep(5+random.random())
                m.click(400,800)
                time.sleep(5+random.random()*2)
                m.click(1596,880)
                time.sleep(5+random.random()*2)
                s = s+1
                    
    if not s<number_to_boss:
        if det_position(5)[2]:
            t = det_position(5)
            m.click(t[0],t[1])
            time.sleep(5+random.random()*2)
            if image_distinguish(pic3,path3):#如果有遇敌，再次点击
                time.sleep(5+random.random())
                m.click(t[0],t[1])
                time.sleep(5+random.random()*2)
            if image_distinguish(pic4,path4):
                if (self_dec_full()):
                    image_distinguish(pic4,path4)

##                while (not det_position(7)[2]):
##                    pass
##                m.click(det_position(7)[0],det_position(7)[1]+400)
                time.sleep(80+random.random()*10)    
                m.click(240,850)
                time.sleep(5+random.random()*2)
                m.click(400,800)
                time.sleep(5+random.random()*2)
                m.click(1596,880)
                time.sleep(5+random.random()*2)
                m.click(1596,880)
                time.sleep(10+random.random()*3)
                s = 0
                print("over")
        else:
            c = c+1
            if c>2:
                s=s-1
                c=0

        
##        time.sleep(2)
##        print("ready",i)
##while True:
##    
####    image_distinguish(pic,path)
##    m.click(position[0],position[1])
##
##    if image_distinguish(pic1,path1):
##        time.sleep(2+random.random()*2)
##        if (self_dec_full()):
##            m.click(position[0],position[1])
##            image_distinguish(pic1,path1)
##        
##        m.click(1350,700)
##        time.sleep(2+random.random()*2)
##        m.click(1630,741)
##        time.sleep(1+random.random())
##        m.click(1520,900)
##        time.sleep(10+random.random()*3)
##
##        i = 0
##        while i<number_to_boss:
##            for j in range(len(loop)):
##                print(j)
##                m.click(loop[j][0],loop[j][1])
##                time.sleep(5+random.random()*3)
##                if image_distinguish(pic3,path3):#如果有遇敌，再次点击
##                    time.sleep(5+random.random()*3)
##                    m.click(loop[j][0],loop[j][1])
##            
##                if image_distinguish(pic4,path4):
##                    if (self_dec_full()):
##                        image_distinguish(pic4,path4)
##                    
##                    time.sleep(50+random.random()*5)
##                    m.click(240,850)
##                    time.sleep(5+random.random())
##                    m.click(400,800)
##                    time.sleep(5+random.random()*2)
##                    m.click(1596,880)
##                    time.sleep(5+random.random()*2)
##                    i = i + 1
##                if not i<number_to_boss:
##                    break
##        
##        #3次后，直接找boss
##        while not image_distinguish(pic4,path4):
##            for k in range(len(boss_position)):
##                m.click(boss_position[k+1][0],boss_position[k+1][1])
##                time.sleep(5+random.random()*2)
##                if image_distinguish(pic3,path3):#如果有遇敌，再次点击
##                    time.sleep(5+random.random())
##                    m.click(boss_position[k+1][0],boss_position[k+1][1])
##                    
##        if (self_dec_full()):
##            image_distinguish(pic4,path4)
##            
##        time.sleep(80+random.random()*10)    
##        m.click(240,850)
##        time.sleep(5+random.random()*2)
##        m.click(400,800)
##        time.sleep(5+random.random()*2)
##        m.click(1596,880)
##        time.sleep(10+random.random()*3)
####            
##        
##

##
##
##
##    
##    
##
##
####弃用部分
##
##
####w = 500
####h = 400
##
##
####temp = 0
####for i in range (len(img)):
####    for j in range(len(img[0])):
####        s = abs(int(img[i][j])-int(img2[i][j]))
####        temp = temp + s*s
####temp = temp/len(img)/len(img[0])
####print(temp)
##
##
####
####a = m.position()    #获取当前坐标的位置
####print(a)
####
####m.move(50,500)
####a = m.position() #鼠标移动到（x,y）位置
####print(a)
####
####m.click(100,1000)  #移动并且在(x,y)位置左击
####
####
####m.click(200,1500,2)  #(300,300)位置右击
##
##

##import numpy as np
##
##
###矩阵相关运算
##def related(mat1,mat2):
##    row1 = len(mat1)#行数
##    col1 = len(mat1[0])#第一个矩阵的列数
##    row2 = len(mat2)#行数
##    col2 = len(mat2[0])
##
##    print(row1)
##    print(col1)
##    print(row2)
##    print(col2)
##    
##    temp = np.zeros([(row1-row2+1),(col1-col2+1)])
##    for i in range(row1-row2+1):
##        for j in range(col1-col2+1):
##            for p in range(row2):
##                for q in range(col2):
##                    temp[i][j] = temp[i][j] + mat1[i+p][j+q]*mat2[p][q]
##    return temp


##
##import matplotlib.pyplot as plt
##import numpy as np
##from scipy import signal
##
####print(datetime.datetime.now())
##
##t = (104,1016)
##t = det_position()
##print(t,t[0],t[1])
##m.move(t[0],t[1])






##a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
##b = np.array([[1,2],[3,4]])#b行或列数不能为1
##b = b-np.mean(b)
##
##
##res = signal.fftconvolve(a,b,mode = 'same')
##print(res)
##posx,posy = divmod(np.argmax(res),res.shape[1])
##
##print(posx)
##print(posx+len(b)-1)
##print(len(b))
##
##x1 = posx+len(b)-1
##y1 = posy+len(b[0])-1
##t1 = a[[posy,y1]]
##print(t1)
##
##t1 = t1[:,[posx,x1]]
##
##print(t1)
