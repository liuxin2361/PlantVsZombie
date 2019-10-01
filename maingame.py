"""
    植物大战僵尸
    version:1.0
"""
import random
import time

import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
VERSION = "v1.0"


# 主程序
class MainGame:
    window = None
    my_pea = None
    background = None
    bullet_list = []
    zobmie_list = []

    def __init__(self):
        pass

    def start_game(self):
        # 初始化主窗口
        pygame.display.init()
        # 设置窗口的大小及显示,返回一个surface对象
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("植物大战僵尸 " + VERSION)
        # 初始化背景
        self.create_background()
        # 初始化豌豆
        self.create_pea()
        while True:
            # 使豌豆移动慢一点，即让循环执行的慢一点，让循环进行沉睡
            time.sleep(0.02)  # 单位是秒
            MainGame.background.back_display()
            self.get_event()
            # 展示豌豆
            MainGame.my_pea.pea_display()
            # 初始化僵尸，并将僵尸添加到列表中
            self.create_zombie()
            # 展示僵尸
            self.blit_zombie()
            # 循环遍历子弹列表,展示子弹
            self.blit_bullet()
            # 调用豌豆移动方法,如果豌豆的移动开关是开启的，豌豆才可以移动
            if MainGame.my_pea and MainGame.my_pea.live:
                if not MainGame.my_pea.stop:
                    MainGame.my_pea.move()
            pygame.display.update()

    def end_game(self):
        exit()

    # 获取事件
    def get_event(self):
        # 获取所有事件
        event_list = pygame.event.get()
        for event in event_list:
            # 如果按下的是退出，就关闭窗口
            if event.type == pygame.QUIT:
                self.end_game()
            # 如果是按下键盘
            if event.type == pygame.KEYDOWN:
                # 当豌豆不存在死亡
                if not MainGame.my_pea:
                    # 判断按下ESC键，让豌豆重生
                    if event.key == pygame.K_ESCAPE:
                        self.create_pea()
                if MainGame.my_pea and MainGame.my_pea.live:
                    if event.key == pygame.K_UP:
                        # 切换方向
                        MainGame.my_pea.direction = "U"
                        # 修改移动开关状态
                        MainGame.my_pea.stop = False
                    elif event.key == pygame.K_DOWN:
                        # 切换方向
                        MainGame.my_pea.direction = "D"
                        MainGame.my_pea.stop = False
                    elif event.key == pygame.K_SPACE:
                        # 按下空格键发射子弹
                        # 创建我方坦克子弹
                        MainGame.my_pea.shot()
            if event.type == pygame.KEYUP:
                # 判断松开的键是方向键时，才停止移动
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.my_pea and MainGame.my_pea.live:
                        MainGame.my_pea.stop = True

    # 初始化背景
    def create_background(self):
        MainGame.background = BackGround(0, 0)

    # 初始化豌豆
    def create_pea(self):
        MainGame.my_pea = Pea(50, 300)

    # 初始化僵尸，并将僵尸添加到列表中
    def create_zombie(self):
        # 随机生成200以内的数
        num = random.randint(1, 200)
        if num < 3:
            zombie = Zombie(SCREEN_WIDTH - 10, random.randint(10, SCREEN_HEIGHT - 70))
            MainGame.zobmie_list.append(zombie)

    # 循环僵尸列表，并展示
    def blit_zombie(self):
        for zombie in MainGame.zobmie_list:
            if zombie.live:
                zombie.zombie_display()
                zombie.move()
            else:
                MainGame.zobmie_list.remove(zombie)

    # 循环遍历子弹列表,展示子弹
    def blit_bullet(self):
        for bullet in MainGame.bullet_list:
            bullet.bullet_display()
            bullet.move()


# 豌豆类
class Pea:
    def __init__(self, left, top):
        # 加载图片
        self.image = pygame.image.load("res/peas.gif")
        # 根据图片surface获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left和top
        self.rect.left = left
        self.rect.top = top
        # 移动方向
        self.direction = "U"
        # 豌豆移动开关
        self.stop = True
        # 存活的状态
        self.live = True

    # 展示豌豆
    def pea_display(self):
        MainGame.window.blit(self.image, self.rect)

    # 射击
    def shot(self):
        my_bullet = Bullet(MainGame.my_pea)
        MainGame.bullet_list.append(my_bullet)

    # 移动
    def move(self):
        if self.direction == "U":
            if self.rect.top > 30:
                # move_ip 可以改变图片的显示对 x,y 的坐标位置
                self.rect.move_ip(0, -10)
        elif self.direction == "D":
            # 距离顶端的距离加上图像的高度要小于窗口的高度
            if self.rect.bottom < SCREEN_HEIGHT - 10:
                self.rect.move_ip(0, 10)


# 僵尸类
class Zombie:
    def __init__(self, left, top):
        # 加载图片
        self.image = pygame.image.load("res/zombie.gif")
        self.image = pygame.transform.scale(self.image, (70, 70))
        # 根据图片surface获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left和top
        self.rect.left = left
        self.rect.top = top
        # 存活的状态
        self.live = True

    def move(self):
        self.rect.move_ip(-2, 0)
        if self.rect.left < 0:
            MainGame.zobmie_list.remove(self)
        else:
            # 撞到豌豆
            if self.rect.colliderect(MainGame.my_pea.rect):
                pygame.quit()
                exit()
            for bullet in MainGame.bullet_list:
                if self.rect.colliderect(bullet.rect):
                    MainGame.bullet_list.remove(bullet)
                    MainGame.zobmie_list.remove(self)
                    break

    def zombie_display(self):
        MainGame.window.blit(self.image, self.rect)


# 豌豆发射的子弹类
class Bullet:
    def __init__(self, pea):
        # 加载图片
        self.image = pygame.image.load("res/bullet.gif")
        # 获取区域
        self.rect = self.image.get_rect()
        self.rect.left = pea.rect.left + pea.rect.width
        self.rect.top = pea.rect.top
        # 子弹的速度
        self.speed = 4

    def move(self):
        # 子弹从屏幕左端水平运动到右边，要判断是否到达右端
        if self.rect.left < SCREEN_WIDTH - 20:
            self.rect.left += self.speed
        else:
            # 到达右端，修改状态
            MainGame.bullet_list.remove(self)

    def bullet_display(self):
        MainGame.window.blit(self.image, self.rect)


# 游戏背景类
class BackGround:
    def __init__(self, left, top):
        # 加载墙壁图片
        self.image = pygame.image.load("res/background.png")
        # 调整背景图片大小 设置和窗口一样大小
        self.scale_image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # 获取背景区域
        self.rect = self.scale_image.get_rect()
        # 设置位置
        self.rect.top = top
        self.rect.left = left

    # 背景显示
    def back_display(self):
        MainGame.window.blit(self.scale_image, self.rect)


if __name__ == '__main__':
    MainGame().start_game()