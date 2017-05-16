import unittest

"""module docstring"""
def my_parse(inputstr):
    """ parse input string to (begin, between, end)"""
    valid_begin = ['01', '02', '03', '04']
    valid_end = ['APPID', 'SN', 'SHA256', 'SHA384', 'EXEC']
    s1_input = inputstr.split(' ', 1)
    begin = s1_input[0]
    # check if begin is valid
    if begin not in valid_begin:
        raise ValueError("invalid begin")
    s2_input = s1_input[-1].rsplit(' ', 1)
    between = s2_input[0]
   
    # check and extract the value
    end = s2_input[-1]
  
    #check the validation of end
    if end not in valid_end:
        raise ValueError("invalid end")

    if begin == '01':
        if len(between) != 16:
            raise ValueError("invalid value")
        else:
            parsed = int(between,16)
    elif begin == '02':
        parsed = end
    elif begin == '03':
        # need check the format of [int32]
        numlist = between.split(' ')
        for num in numlist:
            if len(num) != 8:
                raise ValueError("invalid value")
        parsed = [int(x, 16) for x in numlist]
    elif begin == '04':
        parsed = {'01':True, '00':False}.get(between,'Error')
    else:
        raise ValueError("invalid value")
    result = (begin, between, end)

    print  (parsed)
    return parsed

def my_show(parsed):
    """ show the encode string for given value """
    head = {'ApplicationID':"01 APPID", 'HashAlg':"02 01",
            'SerialNumber': "03 SN", 'AllowExec':"04 EXEC"}

    # target string = head + str(parsed) + tail

    if type(parsed) == int:
        between = str(hex(parsed))
        #remove 0x in the begining of string
        between = between[2:]
        print(between)
        if len(between) != 16:
            raise ValueError("invalid value")
        get_head = head.get('ApplicationID')
        encode = get_head[:2] + ' ' + between + get_head[2:]
    elif type(parsed) == bool:
        between = {True: '01', False:'00'}.get(parsed)
        get_head = head.get('AllowExec')
        encode = get_head[:2] + ' ' + between + get_head[2:]
    elif type(parsed) == list:
        numstr = [str(hex(x))for x in parsed]
        between = ''
        for s in numstr:
            between = between + ' ' + s[2:]
        get_head = head.get('SerialNumber')
        encode = get_head[:2]  + between + get_head[2:]
    elif parsed.upper() in ['SHA256', 'SHA384']:
            encode = head.get('HashAlg') + ' ' + parsed.upper()
      
    else:
        raise ValueError("invalid value")
    
    print(encode)
        
class TestParse (unittest.TestCase):
    def test_01(self):
        self.assertEqual (my_parse('01 12345678abcdef01 APPID'), 0x12345678abcdef01)
    def test_02(self):
        self.assertEqual (my_parse ('02 01 SHA256'), 'SHA256')
    def test_02_02(self):
        self.assertEqual (my_parse ('02 01 SHA384'), 'SHA384')
    def test_03(self):
        self.assertEqual (my_parse('03 12345678 87654321 abcdefab SN'), [0x12345678, 0x87654321, 0xabcdefab])
    def test_04(self):
        self.assertTrue (my_parse('04 01 EXEC'))
    def test_04_02(self):
        self.assertFalse (my_parse('04 00 EXEC'))

if __name__ == "__main__":
    unittest.main()
