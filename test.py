
#
#
# {}
# []
# ()


#如何判断一个字符串里的所有括号都是先左后右
def is_valid_parentheses(s):
    stack = []
    d = {'(':')', '[':']', '{':'}'}
    for c in s:
        if c in d:
            stack.append(c)
        elif c in d.values():
            if not stack or d[stack.pop()] != c:
                return False
    return not stack


if __name__ == '__main__':
  #  print(is_vw yijialid_parentheses('([)]'))

    a=141.379

    b=141.63
    print(abs(a-b)/b)