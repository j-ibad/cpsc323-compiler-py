#!/usr/bin/env python3

#Built-in libs
import sys
import re

#Symbol map, mapping symbols to token types
SYMBOL_MAP = {
    #Keywords
    "int": 1, "float":1, "bool":1, "True":1, "False":1,
    "if":1, "else":1, "then":1, "endif":1, "endelse":1,
    "while":1, "whileend":1, "do":1, "enddo":1, "for":1,
    "endfor":1, "STDinput":1, "STDoutput":1, "and":1, "or":1,
    "not":1,
    
    #Separators
    "(":3, ")":3, "{":3, "}":3, "[":3, "]":3, 
    ",":3, ".":3, ":":3, ";":3,
    
    #Operators
    "*":4, "+":4, "-":4, "=":4, 
    "/":4, ">":4, "<":4, "%":4
}
#Mapping between numerical token types to string form
TOKEN_TABLE = {
    1: "KEYWORD",
    2: "IDENTIFIER",
    3: "SEPARATOR",
    4: "OPERATOR",
    5: "INTEGER",
    6: "FLOAT"
}

#Turns numerical internal notation to string form of token
def numToToken(tokenPairs):
    for i in range(0, len(tokenPairs)):
        tokenPairs[i][0] = TOKEN_TABLE.get(tokenPairs[i][0])


#Performs lexical analysis on the file inputted
def lexer(filename):
    #Open file
    try:
        file = open(filename, "r")
    except:
        print("%s cannot be opened" % filename)
        return [[-1,""]]

    #Init variables
    tokenPairs = []
    wordRegex = "^[a-zA-Z][a-zA-Z0-9_\$]*"
    numRegex = "[+-]?[0-9]+([.][0-9]*)?"
    
    lineNum = 0
    #Traverse file line by line, char by char
    for line in file:
        lineNum+=1
        #print(line)
        ind = 0
        while ind < len(line):
            #Search for next keyword or identifier
            match = re.search(wordRegex, line[ind:])
            #print(match)
            if match is None:   #Keyword or identifier not found
                if line[ind] == "!":    #Comment for rest of line
                    break
                elif line[ind] == " " or line[ind] == "\n" or line[ind] == "\t":  #Ignore space, newline, and tab
                    ind += 1
                    continue
                else:
                    token = SYMBOL_MAP.get(line[ind])
                    if token is None:
                        match = re.search(numRegex, line[ind:])
                        if match is None:
                            print("Not exp 1: [%s]" % line[ind]) #Cant read it
                        else: #Number found
                            if '.' in match.group(): #Is a float
                                tokenPairs.append( [6, match.group(), (lineNum, ind+1)] )
                            else:   # Is a integers
                                tokenPairs.append( [5, match.group(), (lineNum, ind+1)] )
                            ind = match.span()[1] + ind;
                            continue
                    else:   #Detect separators
                        tokenPairs.append( [token, line[ind], (lineNum, ind+1)] )
                ind += 1
                #No matches found
            else:   #Keyword or identifier was found
                while ind < match.span()[0] + ind:
                    print("Not exp 2: %s" % line[ind])
                    ind += 1
                    #Cant read it. Should not reach here.
                
                #Detect indentifiers
                token = SYMBOL_MAP.get(match.group())
                #print("%s is %s" % (match.group(), token))
                if token is None:   #Is an identifier
                    tokenPairs.append( [2, match.group(), (lineNum, ind+1)] )
                else:   #Is a keyword
                    tokenPairs.append( [token, match.group(), (lineNum, ind+1)] )
                
                ind = match.span()[1] + ind;
            
    #Convert nums tokens to string tokens
    numToToken(tokenPairs)
    
    #Return
    return tokenPairs



def main():
    #Accept filename input from command line or prompt
    filename = ""
    if len(sys.argv) <= 1:  #Prompt user for file name
        filename = input("Input filename: ")
    else:   #Accept argument from command line
        filename = sys.argv[1]
    
    #Run lexical analysis function "lexer()"
    tokens = lexer(filename)
    
    #Print tokens
    print("%-16s\t%s\n" % ("TOKENS", "Lexemes"))
    for token, lexeme, loc in tokens:
        print("%-16s=\t%s" % (token, lexeme))
    
    #Return tokens
    return tokens

#Execute main function only when directly executing script
if __name__ == "__main__":
    main()
