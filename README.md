# cpsc323-syntax-analyzer-py
A syntax analyzer for a simple C-like language implemented in python 3. Done as HW 2 for CPSC 323 - Compilers and Languages

Project Name: Project 2 - Syntax Analyzer
Class:  CPSC 323 - 02, Spring 2021
Professor:  Prof. Anthony Le
Authors:    Winnie Pan
            Josh Ibad
            Titus Sudarno
            Thomas-James Le


##Brief Description:
The syntax analyzer uses a top down approach, specifically, using the Recursive Descent Parser method.


##Preconditions:
1. Python 3 is installed in the system and is the version of python being used
2. In order to run the program, it is necessary to keep the following files within the same
directory.
	● lexer.py - Python source code for lexical analysis
	● parser.py - Python source code for syntax analysis
3. Must have read permissions on input files, and permission to write to output file.
4. Filenames may not have commas or trailing whitespace


##Usage:
###i. Synopsis:
Windows: python parser.py <FILE> [<FILE> …] [-o <OUTFILE>]
Linux: python3 parser.py <FILE> [<FILE> …] [-o <OUTFILE>]
or ./parser.py <FILE> [<FILE> …] [-o <OUTFILE>]

###ii. Arguments:
<FILE> 			- Filename or path to input file of source code to be parsed. If one is not
				supplied, the user will be prompted for a file. A list of files may be inputted.
-o <OUTFILE> 	- Name or path to the output file. Defaults to standard output.

###iii. Description:
To execute this program, run the "parser.py" script using the terminal. Make sure to run the
script using Python 3.

From the command line, a file name / path may be inputted in the form "python3
parser.py <file>". A list of input files may be inputted separated by spaces in the form "python3
parser.py <file1> <file2> … <fileN>". If no file is inputted, the program will prompt the user, in
which the user may input a single file, or a list of files separated by commas. Note that when
entering file paths after being prompted, the file path may not have commas, neither leading nor
trailing whitespace. Make sure that there are sufficient read permissions on the input file(s).

The output path may also be specified from the command line by using the -o flag
followed by the output file path. The output file will be overwritten with the tokens, corresponding
production rules, and the parse tree for every input file entered. If no output file is inputted, then
the output defaults to the standard output or console.


##Grammar Rules Used:
	<StatementList> -> <Statement> <StatementList> | <empty>
Assignment
	<Statement> -> <Assign>
	<Assign> -> <ID> = <Expression>
Expressions
	<Expression> -> <Term> | <Term> + <Expression> | <Term> - <Expression>
	<Term> -> <Term> * <Factor> | <Term> / <Factor> | <Factor>
	<Factor> -> '(' <Expression> ')' | <ID> | 'True' | 'False' |
		('+' | '-')?(<FLOAT> | ('.')?<INT>) | //Accept all float forms
Declarations
	<Statement> -> <Declarative>
	<Declarative> -> <Type> <ID> <MoreIds>; | <empty>
	<MoreIds> -> , <ID> <MoreIds> | <empty>
Flow Control Structures
	<Statement> -> if <Conditional> then <StatementList> endif | if
	<Conditional> then <StatementList> else <StatementList> endif
	<Statement> -> while <Conditional> do <StatementList> whileend
	<Statement> -> begin <StatementList> end
	<Conditional> -> <Expression> <Relop> <Expression> | <Expression>
	
	
##Parse Tree:
At the end of each input file's syntax analysis, the resultant parse tree is printed in the format:
["<Non Terminal Symbol 1>" height: X, Children: {
 ["<Non Terminal Symbol of Child>" height: X+1, Children: {
  ['<TOKEN>', '<LEXEME>", (<LINENUM>, <COLNUM>)]
 } End of (<Child>, X+1)]
} End of (<Symbol 1>, X)]

The non terminal symbols are as follows:
	SL = StatementList
	S = Statement
		D = Declarative
			MI = MoreIDs
		A = Assign
			E = Expression
				T = Term
				F = Factor
		C = Conditional
		
		
##Error Handling: 
For any errors encountered during syntax analysis, a meaningful error message is printed, both
in the output file and in the console. The error message contains the filename, the line number
and column number of the token being processed at the time of the error, followed by a
message describing the error, such as what occurred that was unexpected and what the
analyzer was expecting.

After throwing an error message, the syntax analyzer terminates fully and stops processing the
file further.
