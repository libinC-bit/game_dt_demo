
#英雄信息
#棋盘信息包含距离信息、hate信息
#aciton to new state
import time
from copy import copy

import random
class hero:

    def __init__(self, id,name, hp, atk,atk_distance,defense, ap, mp,skill, skill_atk,skill_distance,teamid):
        self.id=id
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.ap= ap
        self.skill=skill
        self.mp=mp
        self.skill_atk=skill_atk
        self.skill_distance=skill_distance
        self.atk_distance=atk_distance
        self.action_=[]
        self.team=teamid
        self.hate_dict={}
        self.x=''
        self.y=''
        self.deaded=False # 20240708 RL训练的时候每一轮游戏结束后，需要重置英雄的状态，而不是新创建一个英雄对象，所以需要一个标记位
    #定义行动列表
    def action_init(self):
        for  i in range(1,self.ap+1):
            self.action_.append('向上移动'+str(i)+'步')
            self.action_.append('向下移动'+str(i)+'步')
            self.action_.append('向左移动'+str(i)+'步')
            self.action_.append('向右移动'+str(i)+'步')


    def add_action_for_enemy(self,enemy):
        self.action_.append('普通攻击'+enemy.name)
        self.action_.append('技能攻击'+enemy.name)

    def get_aciton(self):
        return self.action_


    def attack(self, enemy):
        enemy.hp -= self.atk
        print(f'{self.name}使用普通攻击了{enemy.name}，{enemy.name}剩余血量{enemy.hp}')

        self.hate_dict[(enemy.id,self.id)]=self.hate_dict.get((enemy.id,self.id),0)+self.atk

        print(str(self.name)+'的仇恨值变化:',str(enemy.name)+' 对'+str(self.name)+'的仇恨值增加'+str(self.atk)+'后的仇恨值'+str(self.hate_dict[(enemy.id,self.id)]))

    def skill_attack(self, enemy):
        enemy.hp -= self.skill_atk
        print(f'{self.name}使用技能攻击了{enemy.name}，{enemy.name}剩余血量{enemy.hp}')

        self.hate_dict[(enemy.id,self.id)]=self.hate_dict.get((enemy.id,self.id),0)+self.skill_atk

        print(str(self.name)+'的仇恨值变化:',str(enemy.name)+' 对'+str(self.name)+'的仇恨值增加'+str(self.skill_atk)+'后的仇恨值'+str(self.hate_dict[(enemy.id,self.id)]))

    def move(self, x, y):
        tmp_x=self.x
        tmp_y=self.y

        self.x = x
        self.y = y

        print(f'{self.name} 从[{tmp_x},{tmp_y}] 移动到 [{x} ,{y}]')

class state:
    def __init__(self):
        self.board_h= 15
        self.board_w= 15
        self.board = [[0 for i in range(self.board_w)] for j in range(self.board_h)]
        self.hate_dict={}
        self.atk_distance={}
    def set_hero(self, hero, x, y):
        self.board[x][y] = hero
        hero.x=x
        hero.y=y
    def clc_distance(self):
        for i in range(self.board_h):
            for j in range(self.board_w):
                if self.board[i][j]!=0:
                    for m in range(self.board_h):
                        for n in range(self.board_w):
                            if self.board[m][n]!=0 and self.board[i][j]!=self.board[m][n]:
                                self.atk_distance[(self.board[i][j].id,self.board[m][n].id)]=((i-m),(j-n))

    def clc_hate(self):
        self.hate_dict={}
        for i in range(self.board_h):
            for j in range(self.board_w):
                if self.board[i][j]!=0:
                    #当前的hate_dict增加这个英雄的hate_dict
                    self.hate_dict.update(self.board[i][j].hate_dict)

    #获取当前等state信息
    def get_current_state(self):
        return self.board,self.hate_dict,self.atk_distance




class game:

    def __init__(self):
        self.hero_list=[]
        self.team1='小刘'
        self.team2='强爷'
        hero_A=hero(1,'A',hp=100,atk=5,atk_distance=10,defense=0,ap=2,mp=2,skill='W',skill_atk=20,skill_distance=5,teamid=self.team1)
        self.hero_list.append(hero_A)
        #hero_B=hero(2,'B',hp=100,atk=10,atk_distance=1,defense=5,ap=2,mp=2,skill='W',skill_atk=20,skill_distance=2,teamid=1)
        #self.hero_list.append(hero_B)
        #hero_C=hero(3,'C',hp=200,atk=15,atk_distance=3,defense=5,ap=2,mp=2,skill='W',skill_atk=40,skill_distance=2,teamid=1)
        # self.hero_list.append(hero_C)
        hero_X=hero(4,'X',hp=100,atk=5,atk_distance=10,defense=0,ap=2,mp=2,skill='W',skill_atk=20,skill_distance=5,teamid=self.team2)
        self.hero_list.append(hero_X)
        #hero_Y=hero(5,'Y',hp=100,atk=10,atk_distance=1,defense=5,ap=2,mp=2,skill='W',skill_atk=20,skill_distance=2,teamid=2)
        #self.hero_list.append(hero_Y)
        #hero_Z=hero(6,'Z',hp=200,atk=15,atk_distance=3,defense=5,ap=2,mp=2,skill='W',skill_atk=40,skill_distance=2,teamid=2)
        #self.hero_list.append(hero_Z)
        self.state=state()

    def reset(self):
        for i in range(self.state.board_h):
            for j in range(self.state.board_w):
                self.state.board[i][j]=0
        self.state.hate_dict={}
        self.state.atk_distance={}
        for hero in self.hero_list:
            hero.hp=100
            hero.mp=2
            hero.x=''
            hero.y=''
            hero.deaded=False
            hero.hate_dict={}

    def start(self):

        for hero in self.hero_list:
            hero.action_init()
            for enemy in self.hero_list:
                if hero.team!=enemy.team:
                    hero.add_action_for_enemy(enemy)
            print('英雄名称',hero.name,'所属阵营',hero.team)
            print('英雄可以的行动',hero.get_aciton())

        print('棋盘大小',[self.state.board_h,self.state.board_w])
        #随机选择位置出场，但是不能重叠
        for hero in self.hero_list:
            while 1:
                x=random.randint(0,self.state.board_h-1)
                y=random.randint(0,self.state.board_w-1)
                if self.state.board[x][y]==0:
                    self.state.set_hero(hero,x,y)
                    break
            print('英雄名称',hero.name,'出场位置',[hero.x,hero.y])

    def move_limit_filter(self,hero):

        action_list=copy(hero.get_aciton())
        #time.sleep(4)
        #print('清理前',len(action_list))
        #print('英雄',hero.name,'的行动',action_list)
        for action in hero.get_aciton():
            if '向上' in action:
                step=int(action[-2])
                #print('向上step',step)
                #print(hero.y-step,0)
                if hero.y-step<0:
                    action_list.remove(action)

            if '向下' in action:
                step = int(action[-2])
                #print('向下step',step)
                #print(hero.y+step,self.state.board_h-1)
                if hero.y+step>self.state.board_h-1:
                    action_list.remove(action)
            if '向左' in action:
                step = int(action[-2])
                #print('向左step',step)
                #print(hero.x-step,0)
                if hero.x-step<0:
                    action_list.remove(action)
            if '向右' in action:
                step = int(action[-2])
                #print('向右step',step)
                #print(hero.x+step,self.state.board_w-1)
                if hero.x+step>self.state.board_w-1:
                    action_list.remove(action)
        #print('清理后可用的action_list',len(action_list))
        #time.sleep(4)
        return action_list

    def atk_limit_filter(self,hero):
        action_list=copy(hero.get_aciton())
        for action in hero.get_aciton():
            if '普通攻击' in action:
                for enemy in self.hero_list:
                    if hero.team!=enemy.team:
                        if max(abs(hero.x-enemy.x),abs(hero.y-enemy.y))>hero.atk_distance:
                            action_list.remove(action)
            if '技能攻击' in action:
                for enemy in self.hero_list:
                    if hero.team!=enemy.team:
                        if max(abs(hero.x-enemy.x),abs(hero.y-enemy.y))>hero.skill_distance:
                            action_list.remove(action)
        return action_list


    def check_hero_dead(self):
        for hero in self.hero_list:
            if hero.hp<=0:
                print(hero.name,'死亡')
                self.state.board[hero.x][hero.y]=0
                hero.deaded=True
    def check_game_over(self):
        #检查是否有一方全部死亡
        self.team1_hero_list=[hero for hero in self.hero_list if hero.team==self.team1 and hero.deaded==False]
        self.team2_hero_list=[hero for hero in self.hero_list if hero.team==self.team2 and hero.deaded==False]
        if len(self.team1_hero_list)==0:
            print('游戏结束，',self.team2,'获胜')
            return (True,self.team2)
        if len(self.team2_hero_list)==0:
            print('游戏结束，',self.team1,'获胜')
            return (True,self.team1)
        return (False,'')
    def next(self):

        self.state.clc_distance()
        self.state.clc_hate()

    def action_to_state(self,hero,action):
        #行动转换为新的state
        #action 为英雄的行动
        #返回新的state
        #如果action的文字是 XX移动X步，那么就是移动，调整英雄的位置
        if '向上' in action:
            new_y=hero.y-int(action[-2])
            new_x=hero.x
            hero.move(new_x,new_y)
        if '向下' in action:
            new_y=hero.y+int(action[-2])
            new_x=hero.x
            hero.move(new_x,new_y)
        if '向左' in action:
            new_y=hero.y
            new_x=hero.x-int(action[-2])
            hero.move(new_x,new_y)
        if '向右' in action:
            new_y=hero.y
            new_x=hero.x+int(action[-2])
            hero.move(new_x,new_y)
        self.state.set_hero(hero,hero.x,hero.y)
        #如果action的文字是 XX攻击XX，那么就是攻击，直接执行英雄的函数
        if '普通攻击' in action:
            for enemy in self.hero_list:
                if enemy.name in action:
                    hero.attack(enemy)
        if '技能攻击' in action:
            for enemy in self.hero_list:
                if enemy.name in action:
                    hero.skill_attack(enemy)
        self.check_hero_dead()
    def get_current_herolist(self,teamid):
        return [hero for hero in self.hero_list if hero.team==teamid and hero.deaded==False]

if __name__ == '__main__':
    game=game()
    game.start()
