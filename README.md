# cpsc323-syntax-analyzer-py
A syntax analyzer for a simple C-like language implemented in python 3. Done as HW 3 for CPSC 323 - Compilers and Languages

Project Name: Project 3 - Object Code Generator
Class:  CPSC 323 - 02, Spring 2021
Professor:  Prof. Anthony Le
Authors:    Winnie Pan
            Josh Ibad
            Titus Sudarno
            Thomas-James Le


##Brief Description:
Object code generator with symbol table using scope and type checking.
Conditional:	if (C) then S; endif
				if (C) then S; else S; endif
Loop:			while (C) do S; whileend
Input:			input(id);	!id must have been declared!
Output:			output(E);	

##Preconditions:
1. Python 3 is installed in the system and is the version of python being used
2. In order to run the program, it is necessary to keep the following files within the same
directory.
	● lexer.py - Python source code for lexical analysis
	● parser.py - Python source code for syntax analysis
	● compiler.py - Python source code for object code generation
3. Must have read permissions on input files, and permission to write to output file.
4. Filenames may not have commas or trailing whitespace


##Usage:
###i. Synopsis:
Windows: python compiler.py <FILE> [<FILE> …] [-o <OUTFILE>]
Linux: python3 compiler.py <FILE> [<FILE> …] [-o <OUTFILE>]
or ./compiler.py <FILE> [<FILE> …] [-o <OUTFILE>]

###ii. Arguments:
<FILE> 			- Filename or path to input file of source code to be parsed. If one is not
				supplied, the user will be prompted for a file. A list of files may be inputted.
-o <OUTFILE> 	- Name or path to the output file. Defaults to standard output.

###iii. Description:
To execute this program, run the "parser.py" script using the terminal. Make sure to run the
script using Python 3.

From the command line, a file name / path may be inputted in the form "python3
compiler.py <file>". A list of input files may be inputted separated by spaces in the form "python3
compiler.py <file1> <file2> … <fileN>". If no file is inputted, the program will prompt the user, in
which the user may input a single file, or a list of files separated by commas. Note that when
entering file paths after being prompted, the file path may not have commas, neither leading nor
trailing whitespace. Make sure that there are sufficient read permissions on the input file(s).

The output path may also be specified from the command line by using the -o flag
followed by the output file path. The output file will be overwritten with the tokens, corresponding
production rules, and the parse tree for every input file entered. If no output file is inputted, then
the output defaults to the standard output or console.

The output will be a numbered listing of the object code instructions, followed by a tabular display
of the symbol table (only those of the global scope).


##Data Types:
int = Integer types 
float = Floating point
bool = {"True", "False"}
Operations between different data types are prohibited and will throw a type mismatch error.
Booleans are not allowed in arithmethic operations.


##Flow Control Structures:
Conditional statements:
	if (<conditional>) then
		<statement>;
		...
	endif
	
	if (<conditional>) then
		<statement>;
		...
	else
		<statement>;
		...
	endif
	
Loops:
	while (<conditional>) do
		<statement>;
		....
	whileend


##Symbol Table
The symbol table is represented as a list of dictionaries.
Each dictionary is representative of a scope, with the head of the list being the global scope.
	Once out of scope, a dictionary is popped. Only the global scope is printed.
Each dictionary is a mapping from id to a 2-tuple of (Memory Address, Data Type).
In other words:
	Symbol Table:
	[
		{	id: (memAddr, dataType),
			id2: (memAddr2, dataType),
			... }
		...
	]
The memory addresses start from 5000, and increment for each variable declared.
Access of undeclared variables will throw an error. Scope must be kept in mind.


##Object code
The assembly instructions provided in the class instructions are used.
This includes stack operations, arithmetic operations, compare instructions, jumps, and the label.

Furthrmore, the input and output operations are supported in the form of
	int x;
	input(x); !Puts user input into x!
	output(x+1); !Outputs the results of the expressions x+1!
	

##Error Handling: 
For any errors encountered during compilation, a meaningful error message is printed, both
in the output file and in the console. The error message contains the filename, the line number
and column number of the token being processed at the time of the error, followed by a
message describing the error, such as what occurred that was unexpected and what the
compiler was expecting.

After throwing an error message, the compiler terminates fully and stops processing the
file further.


##Old Notes:
###Grammar Rules Used:
	<StatementList> -> <Statement> <StatementList> | <empty>
Assignment
	<Statement> -> <Assign>
	<Assign> -> <ID> = <Expression>
Expressions
	<Expression> -> <Term> | <Term> + <Expression> | <Term> - <Expression>
	<Term> -> <Factor> * <Term> | <Factor> / <Term> | <Factor>
	<Factor> -> '(' <Expression> ')' | <ID> | 'True' | 'False' |
		('+' | '-')?(<FLOAT> | ('.')?<INT>) | //Accept all float forms
Declarations
	<Statement> -> <Declarative>
	<Declarative> -> <Type> <ID> <MoreIds>; | <empty>
	<MoreIds> -> , <ID> <MoreIds> | <empty>
Conditionals
	<Conditional> -> <Expression> <Relop> <Expression> | <Expression> | (<Conditional>)
Flow Control Structures
	<Statement> -> if <Conditional> then <StatementList> endif | if
		<Conditional> then <StatementList> else <StatementList> endif
	<Statement> -> while <Conditional> do <StatementList> whileend
	<Statement> -> begin <StatementList> end
	
	
###Parse Tree:
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