#!/usr/bin/env python3
'''
Project Name: Project 3 - Intermediate Code Generator
Class:  CPSC 323 - 02, Spring 2021
Professor:  Prof. Anthony Le
Authors:    Winnie Pan
            Josh Ibad
            Titus Sudarno
            Thomas-James Le

'''


import parser
import os
import sys
import re
import getopt

VARIABLE_ADDRESS_START = 5000
compilerFirstFile = True

RELOP_TO_CODE = {">":"GRT", "<":"LES", "==":"EQU", "<>":"NEQ", "<=":"LEQ", ">=":"GEQ"}

class OCG:
    def __init__(self, fIn, fOut, objectCode=[], symbolTables = [{}]):
        self.filename = fIn
        self.parseTree = parser.Parser(fIn, os.devnull) #Outfile is null, surpress parser output
        self.parseTree = self.parseTree.parseTree
        self.memoryCounter = VARIABLE_ADDRESS_START
        self.symbolTables = symbolTables   #Dictionary will have <id>: (<memoryAddress>, <type>)
        self.realStdOut = sys.stdout
        self.objectCode = objectCode
        #File output
        global compilerFirstFile
        if fOut:
            sys.stdout = open(fOut, "w" if compilerFirstFile else "a+")
            compilerFirstFile = False
    
    def generate(self):
        self.SL(self.parseTree)
        
    def close(self):
        sys.stdout = self.realStdOut
        return (self.objectCode, self.symbolTables)
    
    def writeln(self, code):
        self.objectCode.append(code)
        
    # Prints an error message
    def writeError(self, errorMsg, token=[0, 0, [0, 0,]], errorType="Compilation Error"):
        print('%s:%d:%d: %s: %s' % (self.filename, token[2][0], token[2][1], errorType, errorMsg))
        if sys.stdout != self.realStdOut:
            sys.stdout = self.realStdOut
            print('%s:%d:%d: %s: %s' % (self.filename, token[2][0], token[2][1], errorType, errorMsg))
        exit()
        
    
    def SL(self, subtree):
        self.S(subtree.children[0])
        if len(subtree.children) == 3:
            self.SL(subtree.children[2])
        elif len(subtree.children) == 2 and not isinstance(subtree.children[1], list):
            self.SL(subtree.children[1])
        
    def S(self, subtree):
        val = None
        if isinstance(subtree.children[0], list):
            val = subtree.children[0][1]
        else:
            val = subtree.children[0].val
        
        if val == 'D':
            self.D(subtree.children[0])
        elif val == 'A':
            self.A(subtree.children[0])
        elif val == 'if':
            self.symbolTables.append({})
            self.C(subtree.children[1])
            ptr = len(self.objectCode)
            self.SL(subtree.children[3])
            addr1 = len(self.objectCode)+1
            if len(subtree.children) == 7:
                self.objectCode.insert(ptr, "JUMPZ %d" % (addr1+2))
                self.SL(subtree.children[5])
                addr2 = len(self.objectCode)+1
                self.objectCode.insert(addr1, "JUMPZ %d" % (addr2+1))
            else:
                self.objectCode.insert(ptr, "JUMPZ %d" % (addr1+1))
            self.writeln('LABEL')
            self.symbolTables.pop()
        elif val == 'while':
            self.symbolTables.append({});
            addr = len(self.objectCode)
            self.C(subtree.children[1])
            ptr = len(self.objectCode)
            self.SL(subtree.children[3])
            self.writeln("JUMP %d" % (addr+1))
            self.writeln('LABEL')
            addr = len(self.objectCode)
            self.objectCode.insert(ptr, "JUMPZ %d" % (addr+1))
            self.symbolTables.pop()
        elif val == 'begin':
            self.symbolTables.append({})
            self.SL(subtree.children[1])
            self.symbolTables.pop()
        elif val == 'input':
            self.writeln('STDIN')
            tmpID = subtree.children[2][1]
            index = len(self.symbolTables)-1;
            while index >= 0:
                if tmpID in self.symbolTables[index]:
                    tmpMemAddr = self.symbolTables[index][ tmpID ][0]
                    self.writeln("POPM %d" % tmpMemAddr)
                    return self.symbolTables[index][ tmpID ][1]
                else:
                    index -= 1;
            #Undeclared 
            self.writeError("Undeclared identifier: '%s'" % tmpID, subtree.children[2])
        elif val == 'output':
            self.E( subtree.children[2] );
            self.writeln('STDOUT')
        
    def D(self, subtree):
        # Add to symbol table: <id>: (<memAddr>, <type>)
        type = subtree.children[0][1]
        topTable = self.symbolTables[len(self.symbolTables)-1]
        if subtree.children[1][1] in topTable:
            self.writeError("'%s' has already been declared" % subtree.children[1][1], subtree.children[1], "Multiple declaration error")
        topTable[ subtree.children[1][1] ] = ( self.memoryCounter, type )
        self.memoryCounter += 1
        if subtree.children[2] != '<empty>':
            self.MI( subtree.children[2], type )
        
    def MI(self, subtree, type):
        topTable = self.symbolTables[len(self.symbolTables)-1]
        if subtree.children[1][1] in topTable:
            self.writeError("'%s' has already been declared" % subtree.children[1][1], subtree.children[1], "Multiple declaration error")
        topTable[ subtree.children[1][1] ] = ( self.memoryCounter, type )
        self.memoryCounter += 1
        if subtree.children[2] != '<empty>':
            self.MI( subtree.children[2], type )
        
    def A(self, subtree):
        tmpID = subtree.children[0][1]
        index = len(self.symbolTables)-1;
        while index >= 0:
            if tmpID in self.symbolTables[index]:
                tmpMemAddr = self.symbolTables[index][ tmpID ][0]
                type = self.E( subtree.children[2] )
                if type != self.symbolTables[index][ tmpID ][1]:
                    self.writeError("Expecting a %s value, but instead got a %s" % (self.symbolTables[index][tmpID][1], type), subtree.children[0], "Type mismatch error")
                self.writeln("POPM %d" % tmpMemAddr)
                return self.symbolTables[index][ tmpID ][1]
            else:
                index -= 1;
        #Undeclared 
        self.writeError("Undeclared identifier: '%s'" % tmpID, subtree.children[0])
        
    #Leave results in stack
    def E(self, subtree, lastOp=None):
        type = self.T(subtree.children[0])
        if lastOp is not None:
            if lastOp == '+':
                self.writeln('ADD')
            elif lastOp == '-':
                self.writeln('SUB')
        if len(subtree.children) >= 3:
            type2 = self.E( subtree.children[2], subtree.children[1][1] )
            if type == 'bool':  #Write error for arithmetics with booleans
                self.writeError("Arithmetics are invalid for boolean values",  subtree.children[1], "Invalid operation error")
            if type != type2:   #Write error for type mismatch
                self.writeError("Cannot %s a %s with a %s. Types must be equal." % (subtree.children[1][1], type, type2), subtree.children[1], "Type mismatch error")
        return type
        
    def T(self, subtree, lastOp=None):
        type = self.F(subtree.children[0])
        if lastOp is not None:
            if lastOp == '*':
                self.writeln('MUL')
            elif lastOp == '/':
                self.writeln('DIV')
        if len(subtree.children) >= 3:
            type2 = self.T( subtree.children[2], subtree.children[1][1] )
            if type == 'bool':  #Write error for arithmetics with booleans
                self.writeError("Arithmetics are invalid for boolean values",  subtree.children[1], "Invalid operation error")
            if type != type2:   #Write error for type mismatch
                self.writeError("Cannot %s a %s with a %s. Types must be equal." % (subtree.children[1][1], type, type2), subtree.children[1], "Type mismatch error")
        return type
        
    def F(self, subtree):
        node = subtree.children[0]
        if node[1] == '(':
            return self.E(subtree.children[1])
        elif node[0] == 'IDENTIFIER':
            tmpID = node[1]
            index = len(self.symbolTables)-1;
            while index >= 0:
                if tmpID in self.symbolTables[index]:
                    tmpMemAddr = self.symbolTables[index][ tmpID ][0]
                    self.writeln('PUSHM %d' % tmpMemAddr)
                    return self.symbolTables[index][ tmpID ][1]
                else:
                    index -= 1;
            #Undeclared 
            self.writeError("Undeclared identifier: '%s'" % tmpID, subtree.children[0])
        elif node[0] == 'INTEGER':
            self.writeln('PUSHI %s' % node[1])
            return 'int'
        elif node[0] == 'FLOAT':
            self.writeln('PUSHI %s' % node[1])
            return 'float'
        elif node[1] == 'True':
            self.writeln('PUSHI 1')
            return 'bool'
        elif node[1] == 'False':
            self.writeln('PUSHI 0')
            return 'bool'
        else:
            self.writeError("Was expecting (E), id, number, or boolean value.", subtree.children[0], "Invalid factor")
        
    def C(self, subtree):
        #TODO
        node1 = subtree.children[0];
        self.E(node1)
        if len(subtree.children) > 1:
            node2 = None
            tmpRelop = subtree.children[1][1]
            if len(subtree.children) == 3:
                node2 = subtree.children[2]
            elif len(subtree.children) >= 4:
                tmpRelop += subtree.children[2][1]
                node2 = subtree.children[3]
            self.E(node2)
            self.writeln(RELOP_TO_CODE[tmpRelop])


def printCode(objectCode, symbolTables):
    #Print object code
    lineCounter = 1;
    for line in objectCode:
        print("%-5d %s" % (lineCounter, line))
        lineCounter += 1
    #Print Symbol Table
    print("\nSymbol Table")
    print("%16s | %16s | %5s" % ("Identifier", "Memory Address", "Type"))
    print((17*"-")+"|"+(18*"-")+"|"+(5*"-"))
    globalTable = symbolTables[0]
    for id in globalTable:
        print("%16s | %16s | %5s" % (id, globalTable[id][0], globalTable[id][1]))
    
        



def main():
    #Read command line arguments
    mFlags, files = getopt.gnu_getopt(sys.argv[1:], "ho:", ["help"])
    outFile = None

    #Process command line arguments
    for opt, arg in mFlags:
        if opt in ('-h', "--help"):
            print("USAGE: compiler.py <FILE> [<FILE> ...] [-o <OUTFILE>]")
            exit()
        elif opt == '-o':
            outFile = arg
        else:
            print("Option '%s' not recognized" % opt)

    #Prompt for input if none given
    if len(files) < 1:  #Prompt user for file name
        files = input("Input filename(s): ").split(",")
        if files is None or len(files[0]) == 0:
            print("A valid filename must be entered.")
            exit()
        for i in range(0, len(files)):
            files[i] = files[i].strip() #Remove leading and heading whitespace
        if not outFile:
            outFile = input("Output filename (default: console): ")
            if not outFile:
                outFile = None
                print("\tDefaulting to standard output.")

    objectCode = []
    symbolTables = [{}]
    #Perform syntax analysis on all input files
    for filename in files:
        tmpOCG = OCG(filename, outFile, objectCode, symbolTables)
        tmpOCG.generate()
        objectCode, symbolTables = tmpOCG.close()
        #print(objectCode)
    printCode(objectCode, symbolTables)
        


#Execute main function only when directly executing script
if __name__ == "__main__":
    main()
