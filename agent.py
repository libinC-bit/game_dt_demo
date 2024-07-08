import random
import decision_tree
import numpy as np

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




class QLearningAgent:
    def __init__(self, teamid, game, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.teamid = teamid
        self.game = game
        self.act_hero = None
        for hero in self.game.hero_list:
            if hero.team == self.teamid:
                self.act_hero = hero
        self.actions =self.act_hero.get_aciton()
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.q_table = {}  # initialize Q-table
        self.episode = []

    def get_q_value(self, state, action):
        #如果遇到一个新的状态，就将这个状态加入到q表，并且置为0

        if (state, action) not in self.q_table:
            print('这里有一次重新state，get_q_value',state,action)
            self.q_table[(state, action)] = 0.0
        return self.q_table[(state, action)]

    # def update_q_value(self, state, action, reward, next_state):
    #     # update Q value for a state-action pair based on the reward received and the future state
    #     max_q_next_state = max([self.get_q_value(next_state, a) for a in self.actions])
    #     current_q_value = self.get_q_value(state, action)
    #     #Q(s,a)\gets Q(s,a)+\alpha [r+\gamma \underset{a^{'}}{max} Q(s^{'},a^{'})-Q(s,a)]
    #     self.q_table[(state, action)] = current_q_value + self.alpha * (reward + self.gamma * max_q_next_state - current_q_value)

    #MC-RL 只更新结局，反推步骤奖励
    def update_q_value(self, reward):
        # update Q values based on the reward received at the end of an episode
        for state, action in reversed(self.episode):
            if (state, action) not in self.q_table:
                self.q_table[(state, action)] = 0
            self.q_table[(state, action)] = self.alpha * (reward + self.gamma * self.q_table[(state, action)]) + (1 - self.alpha) * self.q_table[(state, action)]
        self.episode = []  # reset the episode list
    def get_action(self, state):
        # epsilon-greedy policy

        action_list_tmp1 = self.game.move_limit_filter(self.act_hero)
        action_list_tmp2 = self.game.atk_limit_filter(self.act_hero)

        action_list = list(set(action_list_tmp1).intersection(set(action_list_tmp2)))
        #游戏内根据游戏规则可以运行的动作列表

        if np.random.uniform(0, 1) < self.epsilon:
            # explore: choose a random action
            action = np.random.choice(action_list)
        else:
            # exploit: choose the action with max Q value for the current state
            #只能从当前state内游戏规则允许的动作中选择
            q_values = {action: self.get_q_value(state, action) for action in action_list}
            max_q_value = max(q_values.values())
            # if multiple actions have the max Q value, randomly choose one of them
            actions_with_max_q_value = [action for action, q_value in q_values.items() if q_value == max_q_value]
            action = np.random.choice(actions_with_max_q_value)

        self.episode.append((state, action))  # add the state-action pair to the episode list
        return action