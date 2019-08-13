

# def hell0():
#     for i in [1,2,3,4,5]:
#         key = yield i
#         print(key)
#
# h = hell0()
#
# print(next(h))
#
# print(h.send(10))
# print(h.send(10))
# print(h.send(10))
# print(h.send(10))


def getContent():
    while True:
        url = yield 'hello'
        print('嘿嘿嘿%s'%url)

def isUrl(g):
    url_list = ['url1','url2','url3']
    for i in url_list:
        g.send(i)

if __name__ == '__main__':
    g = getContent()
    print(next(g))
    isUrl(g)
