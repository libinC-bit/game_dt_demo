import random
import decision_tree
class randomAgent:
    def __init__(self, teamid,game):
        self.teamid=teamid
        self.game=game

    def get_action_hero(self,hero_list):
        #随机选取一个
        self.act_hero=random.choice(hero_list)
        return self.act_hero


    def choice_act(self, state):
        #随机选择一个行动
        action_list_tmp1=self.game.move_limit_filter(self.act_hero)
        #print('行动action过滤后选择',action_list_tmp1)
        action_list_tmp2=self.game.atk_limit_filter(self.act_hero)
        #取交集
        #print('atk action过滤后选择',action_list_tmp2)

        action_list=list(set(action_list_tmp1).intersection(set(action_list_tmp2)))
        #print('合并后',action_list)
        action=random.choice(action_list)

        return action



class DecisionAgent:
    def __init__(self, teamid,game):
        self.teamid=teamid
        self.game=game

    def get_action_hero(self,hero_list):
        #随机选取一个
        self.act_hero=random.choice(hero_list)
        return self.act_hero


    def choice_act(self, state):
        action_list_tmp1=self.game.move_limit_filter(self.act_hero)
        action_list_tmp2=self.game.atk_limit_filter(self.act_hero)

        action_list=list(set(action_list_tmp1).intersection(set(action_list_tmp2)))
        #上述获得了在游戏规则内可以选择的行动,接下来根据state 开始运行决策树执行选择

        board,hate_dict,atk_distance=state.get_current_state()


        descision_info = {'有魔法值': '', '敌人在普通攻击范围内': '','敌人在技能攻击范围内':'', '技能攻击高': '', '敌人在上侧': '','敌人在左侧': '', '敌人在右侧': ''}

        hero_id=self.act_hero.id

        for k in atk_distance.keys():
            v=atk_distance[k]

            if k[0]==hero_id:

                if v[0]>0:
                    descision_info['敌人在上侧']=True
                else:
                    descision_info['敌人在上侧']=False
                if v[1]>0:
                    descision_info['敌人在左侧']=True
                    descision_info['敌人在右侧']=False
                else:
                    descision_info['敌人在左侧']=False
                    descision_info['敌人在右侧']=True
                if min(abs(v[0]),abs(v[1]))<self.act_hero.skill_distance:
                    descision_info['敌人在技能攻击范围内']=True
                else:
                    descision_info['敌人在技能攻击范围内']=False
                if min(abs(v[0]),abs(v[1]))<self.act_hero.atk_distance:
                    descision_info['敌人在普通攻击范围内']=True
                else:
                    descision_info['敌人在普通攻击范围内']=False
        if self.act_hero.mp>0:
            descision_info['有魔法值']=True
        else:
            descision_info['有魔法值']=False

        if self.act_hero.skill_atk>self.act_hero.atk:
            descision_info['技能攻击高']=True
        else:
            descision_info['技能攻击高']=False


        #print('决策信息',descision_info)
        action=decision_tree.make_decision(descision_info)

        #从action_list 里选择名称包含action的行动
        for act in action_list:
            if action in act:
                return act
        #如果都没有 再随机选择一个
        return random.choice(action_list)