# -*- coding: UTF-8 -*-
import sys

from pathlib import Path

#Highlights format support in 20200313
#Programmed by Andy
def readfile(filename):
    #readfile
    with open(filename, mode='r', encoding='UTF-8') as file:
        filereadlines = file.readlines()
    #remove blank lines
    for i in filereadlines:
        if i == '\n':
            filereadlines.remove(i)
    #remove '\n' in line end and middle
    for i in range(len(filereadlines)):
        filereadlines[i] = filereadlines[i].rstrip()
    return filereadlines

def writefile(filename,filereadlines):
    #write file
    newfile = open(filename.with_suffix('.md'), mode='w', encoding='UTF-8')
    newfile.writelines(filereadlines)
    newfile.close()

def converterFromLocalStorage(filename):
    #readfile
    filereadlines = readfile(filename)
    #get '-------------------' line number
    linenum = [1]
    for i in range(len(filereadlines)):
        if '-------------------' in filereadlines[i]:
            linenum.append(i)
    #bookname,author style
    outputfile = []
    outputfile.append('# ' + filereadlines[0][13:-2])
    outputfile.append('**' + filereadlines[1] + '**')

    #converter each highlight block to [][]
    newcontent = []
    for i in range(len(linenum) - 1):
        for j in range(linenum[i] + 1, linenum[i + 1]):
            if filereadlines[j] != '':
                eachcontent.append(filereadlines[j])
        newcontent.append(eachcontent)
    #format eachline to markdown
    #chapter,time,sentence style
    for i in range(len(newcontent)):
        outputfile.append('## ' + newcontent[i][0])
        outputfile.append('*' + newcontent[i][1][3:] + '*')
        outputfile.append('> [原文]' + newcontent[i][2][4:])
        for j in range(3, len(newcontent[i]) - 1):
            outputfile.append('> [原文]' + newcontent[i][j])
        outputfile.append('> [批注]' + newcontent[i][(len(newcontent[i]) - 1)][4:])
    #add blank lines
    for i in range(len(outputfile)):
        outputfile[i] = outputfile[i] + '\n\n'
    #write file
    writefile(filename,outputfile)
            
def converterFromCloud(filename):
    #readfile
    filereadlines = readfile(filename)
    #bookname,author style
    filereadlines[0] = '# ' + filereadlines[0]
    filereadlines[1] = '**' + filereadlines[1] + '**'
    #chapter,time,sentence style
    for i in range(2 , (len(filereadlines) - 3) , 3):
        filereadlines[i] = '## ' + filereadlines[i]
        filereadlines[i + 1] = '*' + filereadlines[i + 1] + '*'
        filereadlines[i + 2] =  '> ' + filereadlines[i + 2]
    filereadlines[len(filereadlines) - 1] = '**' + filereadlines[len(filereadlines) - 1][1:] + '**'
    #add blank lines
    for i in range(len(filereadlines)):
        filereadlines[i] = filereadlines[i] + '\n\n'
    #write file
    writefile(filename,filereadlines)

def main(filename):
    #read file
    file = open(filename, mode='r', encoding='UTF-8')
    firstline = file.readline()

    #Judge highlights from cloud note:onenote and evernote (False) or boox local storage (True)
    fromLocalStorage = 'BOOX读书笔记' in firstline
    if fromLocalStorage:
        converterFromLocalStorage(filename)
    else:
        converterFromCloud(filename)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        for filenames in Path('./').rglob('*.txt'):
            main(filenames)
    elif len(sys.argv) >= 2:
        for i in range(1 , len(sys.argv)):
            main(sys.argv[i])