def setSegmentPageTable(segmentTablelist:[int], PageTablelist:[int]):
    #segment: int, page: int, pagmeframenumber: int,
    pagetable = dict()
    segmenttable = dict()
    freeframelist = list(range(2, 1024))

    for segment, size, frame in zip(segmentTablelist[::3], segmentTablelist[1::3], segmentTablelist[2::3]):
        segmenttable[segment] = [size, frame]
        if frame in freeframelist:
            freeframelist.remove(frame)

    for segment, page, pagmeframenumber in zip(PageTablelist[::3], PageTablelist[1::3], PageTablelist[2::3]):
        if segment not in pagetable.keys():
            pagetable[segment] = {page: pagmeframenumber}
        else:
            pagetable[segment].update({page: pagmeframenumber})
        if pagmeframenumber in freeframelist:
            freeframelist.remove(pagmeframenumber)

    #print('setPageTable')
    return segmenttable, pagetable, freeframelist

def converttoSPW(userValue: int, segmenttable: dict, pagetable: dict, freemframelist: list):
    x = format(userValue, '032b')
    s = x[5:14]
    p = x[14:23]
    w = x[23:]
    pw = x[14:]

    sdecimal = int(str(s),2)
    pdecimal = int(str(p), 2)
    wdecimal = int(str(w), 2)
    pwdecimal = int(str(pw), 2)

    #print(segmenttable)
    #print(pagetable)
    #print(sdecimal,pdecimal,wdecimal)

    if pwdecimal >= segmenttable[sdecimal][0]:
        PA = -1
        tupleofValues = (PA, freemframelist)
        return tupleofValues

    if segmenttable[sdecimal][1] < 0:
        frame = freemframelist.pop(0)
        #b = abs(segmenttable[sdecimal][1])
        #Read disk block b = |PM[2s + 1]|
        #into PM staring at location f2*512:
        #read_block(b, f1*512)
        segmenttable[sdecimal][1] = frame


    if pagetable[sdecimal][pdecimal] < 0:
        frame = freemframelist.pop(0)
        # Read disk block b = |PM[PM[2s + 1]*512 + p]|
        # into PM starting at location f2*512:
        # read_block(b, f2*512)
        pagetable[sdecimal][pdecimal] = frame
    #else:
    #    pagetable[sdecimal] = {pdecimal: pagmeframenumber}

    PA = ( pagetable[sdecimal][pdecimal] * 512) + wdecimal
    tupleofValues = (PA, freemframelist)

    return tupleofValues

#If pw ≥ PM[2s], then report error; VA is outside of the segment boundary
#Else PA = PM[PM[2s + 1]*512 + p]*512 + w
def converttoPA():

    x,y,a = setSegmentPageTable([6,3000,4],[6,5,9])
    z, a  = converttoSPW(1575424, x, y, a)
    q, a = converttoSPW(1575863, x, y, a)
    r, a = converttoSPW(1575864, x, y, a)
    print(z, q, r)
    print(len(a))

    x, y, a = setSegmentPageTable([8, 4000, 3, 9, 5000, -7],[8, 0, 10, 8, 1, -20, 9, 0, 13, 9, 1, -25])
    z, a= converttoSPW(2097162, x, y, a)
    q, a = converttoSPW(2097674, x, y, a)
    r, a = converttoSPW(2359306, x, y, a)
    s, a = converttoSPW(2359818, x, y, a)
    print(z, q, r, s)
    print(len(a))

def Shell_User_input():
	#Shell which will interact as hardware for the Process and Resource Manager
    initfile = open("init-dp.txt", "r")
    initArray = []
    for line in initfile:
        subArray = []
        for word in line.split():
            subArray.append(int(word))
        initArray.append(subArray)
    initfile.close()

    vaValues = []
    infile = open("input-dp.txt", "r")
    outfile = open("output.txt", "w")
    for line in infile:
        for word in line.split():
            vaValues.append(word)

    x,y,a = setSegmentPageTable(initArray[0],initArray[1])

    for VA in vaValues:
        z, a= converttoSPW(int(VA), x, y, a)
        print(z,end=' ',file=outfile)


    outfile.close()


if __name__ == "__main__":
    Shell_User_input()
    #converttoPA()
