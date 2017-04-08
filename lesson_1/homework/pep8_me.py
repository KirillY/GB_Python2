import random
import string # modules were imported one by one, system first


def create_file(namef, dir_, size):# 2 empty lines between top-level func; add trailing underscore to dir to avoid conflict
    '''
    creates a file given size filled with random ascii letters and digits
    '''
    if(size.isdigit()!=True):
            if size.endswith('KB')==True:
                    s1 = size.split('KB')
                    size1 = int(s1[0])*1024
                    token = ''.join(random.choice(string.ascii_uppercase +
                                                  string.ascii_lowercase + string.digits) for x in range(size1))
            if size.endswith('MB')==True:
                    s1 = size.split('MB')
                    size1 = int(s1[0])*1048567
                    token = ''.join(random.choice(string.ascii_uppercase +
                                                  string.ascii_lowercase + string.digits) for x in range(size1))
            if size.endswith('GB') == True:
                    s1 = size.split('GB')
                    size1 = int(s1[0]) * 1073741824
                    token = ''.join(random.choice(string.ascii_uppercase +
                                                  string.ascii_lowercase + string.digits) for x in range(size1))
    else:
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +
                                          string.digits) for x in range(int(size)))

    file = open(dir_ + namef, "w")
    file.write(token)


create_file("\\test1.txt","C:\\Users\\Cactus\\OneDrive\\Edu\\GeekBrains\\Python 2\\hw_project\\lesson_1\\homework",'10KB') # add \\
# create_file("/test2.txt","E:",'1024')
# create_file("/test11.txt","E:",'2MB')
# create_file("/test21.txt","E:",'1B')