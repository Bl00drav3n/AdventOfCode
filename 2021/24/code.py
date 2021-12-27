import math
import random
from multiprocessing import Process, Lock
import time

# NOTE(rav3n): This contains a bunch of leftover testcode. The numbers were found by educated guessing.
# The code was optimized and turned into python code by hand.
# The multiprocessing part is bad, passing memory to a Process just makes a copy instead of sharing the memory. Python
# multiprocessing is cancer, avoid it at all costs!
# You can pass multiple ranges to the work queue and it will check the whole sequence for valid numbers.

THREAD_COUNT = 8

test_input = '''inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2'''

numbers = [
    29989291316519,
    29989291327519,
    29989291338519,
    29989291349519,
    29989292416519,
    29989292427519,
    29989292438519,
    29989292449519,
    29989293516519,
    29989293527519,
    29989293538519,
    29989293549519,
    29989294616519,
    29989294627519,
    29989294638519,
    29989294649519,
    29989295716519,
    29989295727519,
    29989295738519,
    29989295749519,
    29989296816519,
    29989296827519,
    29989296838519,
    29989296849519,
    29989297916519,
    29989297927519,
    29989297938519,
    29989297949519
]

def notshit_isnumeric(a):
    return a.isnumeric() if a[0] != '-' else a[1:].isnumeric()

def inp(state, a):
    state[a] = state['queue'].pop(0)

def add(state, a, b):
    if notshit_isnumeric(b):
        state[a] += int(b)
    else:
        state[a] += state[b]

def mul(state, a, b):
    if notshit_isnumeric(b):
        state[a] *= int(b)
    else:
        state[a] *= state[b]

def div(state, a, b):
    if notshit_isnumeric(b):
        tmp = state[a] / int(b)
    else:
        tmp = state[a] / state[b]
    if tmp >= 0:
        state[a] = int(tmp)
    else:
        state[a] = int(tmp) + 1

def mod(state, a, b):
    if notshit_isnumeric(b):
        state[a] %= int(b)
    else:
        state[a] %= state[b]

def eql(state, a, b):
    if notshit_isnumeric(b):
        state[a] = 1 if state[a] == int(b) else 0
    else:
        state[a] = 1 if state[a] == state[b] else 0

def run_monad(program, n):
    # 'interpreted'
    ALU = {'x': 0,'y':0,'z':0,'w':0,'queue':[int(d) for d in n],'inp':inp,'add':add,'mul':mul,'div': div,'mod':mod,'eql':eql}
    def dispatch(state, args):
        state[args[0]](state, *args[1:])

    for instruction in program:
        dispatch(ALU, instruction.split(' '))
    return ALU['z']

def run_monad_optimized(n):
    # 'compiled'
    digits = [int(d) for d in n]
    x, y, z, w = 0, 0, 0, 0
    a = [ 1, 1, 1, 1, 1, 26, 26, 1,26, 1,26,26, 26,26]
    b = [14,14,14,12,15,-12,-12,12,-7,13,-8,-5,-10,-7]
    c = [14, 2, 1,13, 5,  5,  5, 9, 3,13, 2, 1, 11, 8]
    for i in range(len(n)):
        tmp = z
        z //= a[i]
        w = int(digits[i])
        if b[i] + tmp % 26 != w:
            z = 26 * z + w + c[i]
        print('w = {} z = {} b = {} b+z%26 = {}'.format(w, z, b[i], b[i] + tmp % 26))
    print('MONAD({}) = {}'.format(n,z))
    return z

def run(threadId, work):
    for i in range(work['start'][threadId], work['end'][threadId]):  
        #if i % 1000000 == 0:
        #    print('threadId {} tries {}'.format(threadId, i))
        n = str(i)
        if n.count('0') == 0 and run_monad_optimized(n) == 0:
            print("threadId {} dected a valid number: {}".format(threadId, n))
            #with work['lock']:
                #work['largest'] = max(work['largest'], int(n))
                #print(work['largest'])

def part1(input):
    # NOTE(rav3n): manually trying numbers
    print('Hint: To reduce z, the w value at position i need to line up with the value b[i] + z % 26 for all negative b[i]!')
    print('Hint: Values for positive b[i] can be manipulated freely as long as the above condition can be fulfilled!')
    result = run_monad_optimized(str(19518121316118))
    return
    
    '''
    # NOTE(rav3n): try all of the numbers
    processes = []
    start = [0] * THREAD_COUNT
    end = [0] * THREAD_COUNT
    min_value = int(29989e9)
    max_value = int(29990e9)
    size = (max_value - min_value) // THREAD_COUNT
    work = {'min':min_value, 'start':start, 'end':end, 'lock':Lock(), 'largest':0}
    work['program'] = input.strip().split('\n')

    t0 = time.time_ns()
    for i in range(THREAD_COUNT):
        work['start'][i] = min_value + i * size
        work['end'][i] = max_value if i == THREAD_COUNT - 1 else work['start'][i] + size
        p = Process(target=run, args=(i, work))
        processes.append(p)
    
    for p in processes:
        p.start()
        p.join()
    t1 = time.time_ns()
    dt = (t1 - t0) // 1e9

    print("Part 1: The largest accepted model number is {} ({:.1f}sec)".format(work['largest'], dt))
    '''

def part2(input):
    print("Part 2:".format())

if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.read()
        print('---INPUT---')
        part1(input)