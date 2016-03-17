from reads_dict import flatten_nested_list_dict, ReadIdGen


def test_flatten_nested_list_dict():
    assert flatten_nested_list_dict({
        1: {
            2: {
                3: ['a'],
                4: ['b'],
            },
            5: ['c'],
        },
        6: ['d'],
        7: [],
        8: {
        },
    }) == \
        {1: ['a', 'b', 'c'],
         6: ['d'],
         7: [],
         (1,): ['a', 'b', 'c'],
         (1, 2): ['a', 'b'],
         (1, 2, 3): ['a'],
         (1, 2, 4): ['b'],
         (1, 5): ['c'],
         (6,): ['d'],
         (7,): []}


def test_ReadIdGen():
    rig = ReadIdGen()
    l = [str(rig) for i in xrange(3)]
    assert len(set(l)) == len(l)
    assert len(set([len(x) for x in l])) == 1


def test_ReadIdGen2():
    rig = ReadIdGen()
    l = [str(rig) for i in xrange(2)]
    assert l[1] == "M00321:123:000000000-ABCDE:1:1111:22222:00002"
