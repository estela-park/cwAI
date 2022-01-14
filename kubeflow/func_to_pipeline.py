import kfp
from kfp.components import func_to_container_op
from kfp.components import create_component_from_func

@func_to_container_op
def test_fn():
    print('it is formed')
    

print(type(test_fn()))

def fn_op():
    print('you can build component this way too')
    
    
# comp_fn = create_component_from_func(fn_op, output_component_file='trial.yaml')
# print(type(comp_fn))

def py_vanilla(a, b):
    print(a+b)

def py_vanilla_no_return():
    x = 3 + 4

fn_literal = py_vanilla

fn_literal2 = py_vanilla_no_return

print(type(py_vanilla))
print(type(fn_literal))
print(type(py_vanilla_no_return))
print(type(fn_literal2))


def make_adder(n):
    def add(x):
        print(x)
        return x + n
    print(n)
    return add

plus_3 = make_adder(3)
# 3은 n의 자리로 들어간다
print(plus_3)
# <function make_adder.<locals>.add at 0x000001C9FEB62C10>

plus_3(4)
# 4는 x자리로 들어간다
# make_adder()가 add를 반환하기 때문에 plus_3의 arg는 add()의 안쪽이다.

print(type(plus_3))
# <class 'function'>
print(type(plus_3(5)))
# <class 'int'>
# plus_3호출시 n=3 env가 이미 성립되어 있기 때문에 print(n)은 실행되지 않는다
# n==3 is a given
# def plus_3(x): 
#     print(x)
#     return x + 3
# 과 같으며 위의 3은 plus_3이 선언되는 순간(make_adder(3)) 결정된다(lexical scope)

class callable_object:
    def __init__(self, num):
        print('you just construct me')
        self.num = num
    def __call__(self, x):
        print('did you call me?')
        return self.num + x

callable_object(3)
# you just construct me
callable_object(4)(5)
# you just construct me
# did you call me?

print(callable_object(4).num)
print(type(callable_object(4).num))

class vanilla_obj():
    def __init__(self, num):
        print('you just construct me')
        self.num = num

print(callable(callable_object(3)))#    True
print(callable(vanilla_obj(4)))#        False
print(callable(plus_3))#                True