#!/bin/env  python
handler=open("1.log","r")
rt_dict={}
while  True:
    x=handler.readline()
    if x == "":
        break


#    if x == '11ab':
#        break
    node=x.split(" ")
#    #print node
#    print node1
#       #shandler.write(node)
    ip,url,code=node[3],node[6],node[12]
    key=(ip,url,code)
    if key  not in  rt_dict:
        rt_dict[key]=1
    else:
        rt_dict[key]=rt_dict[key]+1
#print len(rt_dict)
#print rt_dict
handler.close()
list1=rt_dict.items()
#print list1[0]
#print list1[1]
#print list1[2]

#print  len(list1)
for  m  in  range(0,3):
    for  n   in range(m+1,len(list1)):
        if list1[m][1] > list1[n][1]:
            temp=list1[n]
            list1[n]=list1[m]
            list1[m]=temp
print  list1[-1:-4:-1]
