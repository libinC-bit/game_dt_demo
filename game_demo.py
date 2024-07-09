
import random
import time
import game_info
import agent


def main(timp_sleep=1):

    game=game_info.game()
    agent_liu=agent.randomAgent('小刘',game)
    agent_qiang=agent.randomAgent('强爷',game)
    game.start()
    while True:

        time.sleep(timp_sleep)
        agent_liu.act_hero=agent_liu.get_action_hero(game.get_current_herolist('小刘'))
        action=agent_liu.choice_act(game.state)
        print(agent_liu.act_hero.team,'选择了',agent_liu.act_hero.name,'选择行动是:',action)
        game.action_to_state(agent_liu.act_hero,action)
        game_status,team=game.check_game_over()
        if game_status:
            return team


        game.next()


        time.sleep(timp_sleep)
        agent_qiang.act_hero=agent_qiang.get_action_hero(game.get_current_herolist('强爷'))
        action=agent_qiang.choice_act(game.state)
        print(agent_qiang.act_hero.team,'选择了',agent_qiang.act_hero.name,'选择行动是:',action)

        game.action_to_state(agent_qiang.act_hero,action)
        game_status, team = game.check_game_over()
        if game_status:
            return team
        game.next()

def main_with_decision(timp_sleep=1):

    game=game_info.game()
    agent_liu=agent.randomAgent('小刘',game)
    agent_qiang=agent.DecisionAgent('强爷',game)
    game.start()
    game.next()
    while True:

        time.sleep(timp_sleep)
        agent_liu.act_hero=agent_liu.get_action_hero(game.get_current_herolist('小刘'))
        action=agent_liu.choice_act(game.state)
        print(agent_liu.act_hero.team,'选择了',agent_liu.act_hero.name,'选择行动是:',action)
        game.action_to_state(agent_liu.act_hero,action)
        game_status,team=game.check_game_over()
        if game_status:
            return team

        game.next()

        time.sleep(timp_sleep)
        agent_qiang.act_hero=agent_qiang.get_action_hero(game.get_current_herolist('强爷'))
        action=agent_qiang.choice_act(game.state)
        print(agent_qiang.act_hero.team,'选择了',agent_qiang.act_hero.name,'选择行动是:',action)

        game.action_to_state(agent_qiang.act_hero,action)
        game_status, team = game.check_game_over()
        if game_status:
            return team
        game.next()


def main_with_Qlearning(timp_sleep=1):

    game=game_info.game()
    agent_liu=agent.randomAgent('小刘',game)
    agent_qiang=agent.QLearningAgent('强爷',game)
    game.start()
    game.next()
    while True:

        time.sleep(timp_sleep)


        agent_liu.act_hero = agent_liu.get_action_hero(game.get_current_herolist('小刘'))
        action = agent_liu.choice_act(game.state)
        print(agent_liu.act_hero.team,'选择了',agent_liu.act_hero.name,'选择行动是:',action)

        game.action_to_state(agent_liu.act_hero, action)
        game_status, team = game.check_game_over()

        if game_status:
            agent_qiang.update_q_value(reward=-1)
            return team

        game.next()


        time.sleep(timp_sleep)
        state = game.state

        action = agent_qiang.get_action(state)
        print(agent_qiang.act_hero.team,'选择了',agent_qiang.act_hero.name,'选择行动是:',action)
        game.action_to_state(agent_qiang.act_hero,action)
        game_status, team = game.check_game_over()
        if game_status:
            agent_qiang.update_q_value(reward=1)
            return team
        game.next()

if __name__ == '__main__':
    main_with_decision(0)
    #
    # n=100
    # res_list=[]
    # for i in range(n):
    #     res=main_with_decision(0)
    #     res_list.append(res)
    # #统计结果
    # print('小刘获胜次数:',res_list.count('小刘'))
    # print('强爷获胜次数:',res_list.count('强爷'))

    # n=100
    # res_list=[]
    # for i in range(n):
    #     res=main_with_Qlearning(0)
    #     res_list.append(res)
    #     time.sleep(199)
    # print('小刘获胜次数:', res_list.count('小刘'))
    # print('强爷获胜次数:', res_list.count('强爷'))

