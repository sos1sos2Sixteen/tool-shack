import traceback
import argparse

import tool_shack.debug as debug
import tool_shack.core as core 
import tool_shack.scripting as scripting
import tool_shack.data as data

from tool_shack.debug import testcase

def tprint(*args, **kwargs): 
    print('  ', end='')
    print(*args, **kwargs)


@testcase()
def test_package(): 
    assert core._sanity_check(2) == 3

@testcase()
def test_aggregator(): 
    import os.path as osp
    root_dir = 'some_where'
    with scripting.AggregateVars() as agg: 
        folder_1 = osp.join(root_dir, 'pretrained')
        subfolder = osp.join(folder_1, 'designations')
        folder_2 = osp.join(root_dir, 'events')
    for dir in agg: 
        tprint(f'{dir} exists: {osp.exists(dir)}')

@testcase(should_fail=True)
def failed_successfully(): 
    raise NotImplementedError()

@testcase()
def agg_funcs(): 
    with scripting.AggregateVars() as agg: 
        def f(): 
            return 0
        def g(): 
            return 1
    for h in agg: 
        tprint(h.__name__, h())

@testcase()
def test_bigand(): 
    assert core.big_and((True, True, True)) == True
    assert core.big_and([False, True, True]) == False
    assert core.contains_all(
        (1, 2), [1, 3, 4, 5]
    ) == False
    assert core.contains_all(
        [1, 2], (1, 2, 3)
    ) == True


@testcase()
def test_null(): 
    core.nullcall()
    core.nullcall(1, 2, 3, abc=3)

@testcase()
def test_unique(): 
    xs = [1,1,1,1,1,2,2,2,2,6,7,8]
    assert [1,2,6,7,8] == core.tell(tprint, list(data.unique_filter(xs)))
    assert [1,2,2,8] == core.tell(tprint, data.take_every(3, xs))

@testcase()
def test_indices(): 
    import copy

    xs = [
        (1, 'one'),
        (2, 'two'), 
        (3, 'three')
    ]

    dxs = copy.copy(xs)
    dxs.append((3, 'another three'))
    getter = lambda x: x[0]

    index_res = {
        1 : (1, 'one'),
        2 : (2, 'two'), 
        3 : (3, 'three')
    }

    group_res = {
        1 : [(1, 'one')],
        2 : [(2, 'two')], 
        3 : [(3, 'three'), (3, 'another three')]
    }

    assert core.tell(tprint, data.index_by(getter, xs)) == index_res
    assert data.group_by(getter, dxs) == group_res

    assert data.reduce_group(
        lambda xs: sum([x[0] for x in xs]), group_res
    ) == {
        1: 1,
        2: 2,
        3: 6
    }

def test_find_attr(): 
    import re
    class A(): 
        def test_a(self): 
            '''doc string for method `a`'''
            pass
        def test_b(self): 
            '''doc string for method b'''
            pass

    debug.find_attr(A(), 'test')
    debug.find_attr(A(), re.compile('test'))

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print stack trace on error')
    args = parser.parse_args()


    n_failed = 0
    test_cases = [
        test_package, 
        test_aggregator,
        failed_successfully,
        agg_funcs,
        test_bigand,
        test_null,
        test_unique,
        test_indices,
        test_find_attr,
    ]

    for case in test_cases: 
        try: 
            case()
        except Exception as e: 
            n_failed += 1
            print(f'case failed with {type(e)}')
            if args.verbose: 
                print(traceback.format_exc())

    if n_failed == 0: 
        print(f'all tests passed succesfully!')
    else : 
        print(f'{n_failed} tests failed, rerun with -v flag for a stack trace')


if __name__ == '__main__': 
    main()
    pass

