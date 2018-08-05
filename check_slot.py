#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2018-08-05 21:46:02

# File Name: checkSlot.py
# Description:

"""
def calculate_slot(key_name):
    """return the slot id which the key belongs"""
    from PyCRC.CRCCCITT import CRCCCITT
    crc_value = CRCCCITT().calculate(str(key_name))
    print crc_value % 16384
    return crc_value % 16384

def _get_16384_slot_id(prefix="qatest_"):
    """get 16384 keys which can cover 16384 slots."""
    slot_set = set()
    slot_dict = dict()
    for num in range(1, 1000000, 1):
       key = prefix + str(num)
       slot_id = calculate_slot(key)
       if slot_id not in slot_set:
           slot_set.add(slot_id)
           slot_dict[slot_id] = key
       if len(slot_set) == 16384:
           break
    if len(slot_dict) > 0:
        sorted_slot_dict = sorted(slot_dict.iteritems(), key=lambda d:d[0])
        return sorted_slot_dict
    else:
        return False

def gen_16384key(prefix="qatest_"):
    slot_dict = _get_16384_slot_id(prefix)
    if slot_dict:
        with open("slot_key.md", "w") as sk:
            for key,value in slot_dict:
                sk.write("%s  %s\n" % (key ,value))

if __name__ == "__main__":
    import sys, inspect
    if len(sys.argv) < 2:
        print "Usage:"
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                          str(["%s=%s" % (a, b) for a, b in zip(args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try:
            r = func(*args)
        except Exception, e:
            print "Usage:"
            print "\t", "python %s" % sys.argv[1], str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)
