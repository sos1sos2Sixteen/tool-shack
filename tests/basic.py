import tool_shack.core as core

def test_package(): 
    assert core.add_one(2) == 3

if __name__ == '__main__': 
    test_package()