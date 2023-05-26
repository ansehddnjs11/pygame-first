import pygame
import random
import time
from datetime import datetime

# 1. 게임 초기화
pygame.init()

# 2. 게임 창 옵션 설정
size = [400, 600]
screen = pygame.display.set_mode(size)  #window size

title = "My Game"
pygame.display.set_caption(title)   #title

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()
    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img,(sx,sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x,self.y))
        
# a.x - b.sx <= b.x <= a.x+a.sx
# a.y - b.sy <= b.y <= a.y+a.sy
def crash(a, b):
    if a.x - b.sx <= b.x and b.x <= a.x + a.sx:
        if a.y - b.sy <= b.y and b.y <= a.y + a.sy:
            return True
        else:
            return False
    else: return False
    

ss = obj()
ss.put_img('pygame\gogo\images.png')
ss.change_size(50,80)
ss.x = round((size[0] - ss.sx) / 2)
ss.y = size[1] -ss.sy - 15
ss.move = 5

left_go = False
right_go = False
space_go = False

m_list = []             #생성된 미사일을 리스트에 저장
a_list = []

black = (0, 0, 0)   #rgb
white = (255, 255, 255)
k = 0

kill = 0
loss = 0

# 4. 메인 이벤트
start_time = datetime.now()
SB = 0  #종료시 SB 값 변경
while SB == 0:  #항상 실행할 수 있게

    # 4-1. FPS 설정
    clock.tick(60)  #fps 는 60으로 설정
    
    # 4-2. 각종 입력 감지
    #키보드나 마우스의 동작을 받는 함수. 키보드 여러개를 동시에 누를 수 있으니 리스트로 저장이 되있음. 따라서 event를 받아서 for문으로 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1                     
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ss.x -= ss.move
                left_go = True
            elif event.key == pygame.K_RIGHT:
                ss.x += ss.move
                right_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                ss.x -= ss.move
                left_go = False
            elif event.key == pygame.K_RIGHT:
                ss.x += ss.move
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False
    
    # 4-3. 입력, 시간에 따른 변화
    now_time = datetime.now()
    if left_go == True:
        ss.x -= ss.move
        if ss.x <= 0 :
            ss.x = 0
    elif right_go == True:
        ss.x += ss.move
        if ss.x >= size[0] - ss.sx:
            ss.x = size[0] - ss.sx
    
    if space_go == True and k % 6 == 0:    #미사일 생성만 미사일 생성은 스페이스바를 눌렀을때..
        mm = obj()
        mm.put_img('pygame\gogo\missile.jpg')
        mm.change_size(5, 15)
        mm.x =  round(ss.x + ss.sx / 2 - mm.sx / 2)
        mm.y = ss.y - mm.sy - 10
        mm.move = 15
        m_list.append(mm)

    k += 1    
    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y <= -m.sy:
            d_list.append(i)
    
    for d in d_list:
        del m_list[d]
    
    d_list = []        
    if random.random() > 0.98:
        aa = obj()
        aa.put_img('pygame\gogo\missile.jpg')
        aa.change_size(40, 40)
        aa.x = random.randrange(0, size[0] - aa.sx)
        aa.y = 10
        aa.move = 1
        a_list.append(aa)
    
    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
    for d in d_list:
        del a_list[d]
        loss += 1
        
    dm_list = []
    da_list = []
    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m,a):
                dm_list.append(i)
                da_list.append(j)
    dm_list = list(set(dm_list))    #중복 제거 (미사일 두개가 하나의 에일리언 혹은 하나의 미사일이 두개의 에일리언)
    da_list = list(set(da_list))
    
    for dm in dm_list:
        del m_list[dm]
    for da in da_list:
        del a_list[da]
        kill += 1
        
    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a,ss):
            SB = 1
            time.sleep(1)
    
    # 4-4. 그리기
    screen.fill(black)
    ss.show() #이미지를 0,0에 그려줌
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()
        
    font = pygame.font.Font('C:/WINDOWS/FONTS/ARLRDBD.TTF', 20)
    text = font.render(f"killed : {kill} loss : {loss}", True, (255,255,0))
    screen.blit(text, (10,5))
    
    # 4-5. 업데이트
    pygame.display.flip()   #무조건 필요. 화면을 업데이트 해주는 함수
    
# 5. 게임 종료
pygame.quit()
