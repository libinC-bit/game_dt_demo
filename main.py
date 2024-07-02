


#对战的过程:
#1、全局一个轮询周期
#1、每个棋子X 生成一个预置的行动决策树
#2、轮到当前棋子X行动的时候,先收集当前的相关所需的环境信息
#3、根据当前的环境信息，对当前的行动决策树进行一次遍历，得到每个行动决策的分数
#4、选择分数最高的行动决策，执行
#5、执行完毕后，更新环境信息




class Node:
    def __init__(self, decision_function, left=None, right=None):
        self.decision_function = decision_function
        self.left = left
        self.right = right
#给我一个函数创建一个最优二叉树
def create_tree():
    node7 = Node(lambda state: '释放W')
    node9 = Node(lambda state: '释放Y')
    node8 = Node(lambda state: state['W可释放'],left=node7,right=node9)

    # 6、如果敌人A在攻击范围内，可以攻击敌人A，但是没有魔法，就普通攻击
    node6 = Node(lambda state: '普通攻击')


    # 4、如果敌人A在攻击范围内，可以攻击敌人A，并且有魔法值可以释放技能，优先释放技能W
    node4 = Node(lambda state: state['有魔法值'], node8,node6)

    # 3、如果敌人A在攻击范围外，且其他敌人也在攻击范围外，优先向A移动
    node3 = Node(lambda state:'向A移动')

    # 1、如果敌人A在攻击范围内，优先攻击敌人A
    root = Node(lambda state: state['A在攻击范围内'], left=node4, right=node3)

    return root

def get_action(tree, state):
    node = tree
    while node.left or node.right:
        if node.decision_function(state):
            node = node.left
        else:
            node = node.right
        print('寻找到',node.decision_function)
    return node.decision_function(state)

def print_tree(node, indent=0):
    print('  ' * indent + str(node.decision_function.__code__.co_consts))
    if node.left:
        print('  ' * (indent + 1) + 'Y:')
        print_tree(node.left, indent + 2)
    if node.right:
        print('  ' * (indent + 1) + 'N:')
        print_tree(node.right, indent + 2)
if __name__ == '__main__':
    tree = create_tree()
    state = {'A在攻击范围内': True, '有魔法值': False, 'W可释放': False}
    action = get_action(tree, state)
    print(action)
    #print_tree(tree)