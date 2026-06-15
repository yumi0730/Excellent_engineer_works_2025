"""
这个是小车代码的主函数，总体逻辑是初始化，等待按钮按下，刷新摄像头，确保到读取aprilag码信息，启动小车的apriltag码巡航功能，到达一定条件停止apriltag码巡航
"""
from oled_2 import oled
from pathlib import Path
from camera_1 import paizhao
from servo_2 import lunzi
from oled_2 import oled
from yolo_0 import my_yolo
from start import qidong
import cv2

def refresh_camera(cam,distance,flag):
    while(True):
        datas = cam.estimate_pose_and_location()
        if(datas):
            t_vector = datas[0][2]
            z_distance = t_vector[2]
            tag = datas[0][3]
            if(flag == "min"):     
                if(z_distance > distance):
                    break
            elif(flag == "max"):
                if(z_distance < distance):
                    break
    return z_distance,tag

def car_forward_fast(x_distance,x_pianzhuan,duoji):
    t = 0
    if(x_distance < -0.00):
        duoji.control(60,77,t)
    elif(x_distance > 0.00):
        duoji.control(100,62,t)
    else:
        # if(x_pianzhuan < -0.1):
        #     duoji.control(60,77,t)
        # elif(x_pianzhuan > 0.1):
        #     duoji.control(100,62,t)
        # else:
        pass
    
def car_back_fast(x_distance,x_pianzhuan,duoji):
    t = 0
    if(x_distance < -0.06):
        duoji.control(-100,-51.5,t)#向左
    elif(x_distance > 0.06):
        duoji.control(-60,-72,t)#向右
    else:
        if(x_pianzhuan < -0.05):
            duoji.control(-100,-51.5,t)
        elif(x_pianzhuan > 0.05):
            duoji.control(-60,-72,t)
        else:
            pass
    
def xunji(cam,duoji,temp,flag):
    while(True):
        datas = cam.estimate_pose_and_location()
        if(datas):
            r_vector = datas[0][1];t_vector = datas[0][2];x_pianzhuan = r_vector[1];z_distance = t_vector[2];x_distance = t_vector[0];tag = datas[0][3]
            if(flag == "back"):
                if(z_distance >= temp):
                    break
                car_back_fast(x_distance,x_pianzhuan,duoji)
            elif(flag == "forward"):
                if(z_distance <= temp):
                    break
                car_forward_fast(x_distance,x_pianzhuan,duoji)
            print(f"x_distance={x_distance},x_pianzhuan={x_pianzhuan}")
    return tag,z_distance

def main():
    paizhao1 = paizhao();lunzi1 = lunzi();pingmu1 = oled();
    shibie = my_yolo()

    qidong()
    print("启动成功")
    distance_max_1,r = refresh_camera(paizhao1,0.33,"min")
    pingmu1.draw_id(r)
    lunzi1.control(54,60,0.5)
    _,a = xunji(paizhao1,lunzi1,0.23,"forward")
    lunzi1.control(0,0,0.1)
    if(r == 64):
        lunzi1.control(-40,50,1)#向左
    elif(r == 65):
        lunzi1.control(35,-50,0.9)#向右
    lunzi1.control(0,0,1)
    distance_max_2,_ = refresh_camera(paizhao1,0.23,"min")
    er,b = xunji(paizhao1,lunzi1,0.5,"forward")
    print(er)
    lunzi1.control(0,0,0.1)
    ret,img = paizhao1.camera.read()
    if(ret):
        cv2.imwrite("nihao1.jpg",img)
        wuping = shibie.run(img)
        print(wuping)
        if(len(wuping)==6):
            pingmu1.draw_wuti(wuping,er,r)
    print("-----------------")
    _,a = xunji(paizhao1,lunzi1,distance_max_2 - 0.04,"back")
    lunzi1.control(0,0,0.1)
    if(r == 64):
        lunzi1.control(35,-50,1)#向左
    elif(r == 65):
        lunzi1.control(-40,50,0.9)#向右
    lunzi1.control(0,0,0.1)
    refresh_camera(paizhao1,0.3,"max")
    _,temp = xunji(paizhao1,lunzi1,distance_max_1 - 0.05,"back")
    lunzi1.control(-0.05,-0.05,0.01)
    lunzi1.control(0,0,1)
    # lunzi1.control(-80,-100,1)
    # lunzi1.control(0,0,1)
    print(a)
    print(distance_max_1)
    pingmu1.draw_done()
    lunzi1.control(0,0,5)

def test():
    paizhao1 = paizhao()
    lunzi1 = lunzi()
    # lunzi1.control(72,100,10)
    lunzi1.control(-80,-100,10)

if __name__ =="__main__":

    main()
