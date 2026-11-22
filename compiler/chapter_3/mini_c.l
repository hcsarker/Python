/* 
 * mini_c.l - Flex specification for Mini-C Lexical Analyzer
 * CIT 412: Compiler Design and Automata Theory Sessional
 * Chapter 3: Section 3.5
 *
 * Compilation instructions (using Flex and GCC):
 *   flex mini_c.l
 *   gcc lex.yy.c -o mini_c_lexer
 *   ./mini_c_lexer < input.c
 */

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int line_num = 1;
int word_count = 0;
int char_count = 0;
%}

/* Regular definitions */
delim       [ \t\r]
ws          {delim}+
letter      [A-Za-z_]
digit       [0-9]
id          {letter}({letter}|{digit})*
number      {digit}+(\.{digit}+)?([eE][+-]?{digit}+)?

%x COMMENT

%%

"/*"                { BEGIN(COMMENT); }
<COMMENT>"*/"       { BEGIN(INITIAL); }
<COMMENT>\n         { line_num++; }
<COMMENT>.          { /* skip comment body */ }

"//".*              { /* skip single-line comments */ }

\n                  { line_num++; char_count++; }
{ws}                { char_count += yyleng; }

"int"               { printf("<KW_INT, -> (line %d)\n", line_num); char_count += yyleng; word_count++; }
"float"             { printf("<KW_FLOAT, -> (line %d)\n", line_num); char_count += yyleng; word_count++; }
"char"              { printf("<KW_CHAR, -> (line %d)\n", line_num); char_count += yyleng; word_count++; }
"if"                { printf("<KW_IF, -> (line %d)\n", line_num); char_count += yyleng; word_count++; }
"else"              { printf("<KW_ELSE, -> (line %d)\n", line_num); char_count += yyleng; word_count++; }
"while"             { printf("<KW_WHILE, -> (line %d)\n", line_num); char_count += yyleng; word_count++; }
"return"            { printf("<KW_RETURN, -> (line %d)\n", line_num); char_count += yyleng; word_count++; }

"<="                { printf("<RELOP, LE> (line %d)\n", line_num); char_count += 2; }
">="                { printf("<RELOP, GE> (line %d)\n", line_num); char_count += 2; }
"=="                { printf("<RELOP, EQ> (line %d)\n", line_num); char_count += 2; }
"!="                { printf("<RELOP, NE> (line %d)\n", line_num); char_count += 2; }
"<"                 { printf("<RELOP, LT> (line %d)\n", line_num); char_count += 1; }
">"                 { printf("<RELOP, GT> (line %d)\n", line_num); char_count += 1; }
"="                 { printf("<ASSIGN, => (line %d)\n", line_num); char_count += 1; }

"+"                 { printf("<ARITHOP, +> (line %d)\n", line_num); char_count += 1; }
"-"                 { printf("<ARITHOP, -> (line %d)\n", line_num); char_count += 1; }
"*"                 { printf("<ARITHOP, *> (line %d)\n", line_num); char_count += 1; }
"/"                 { printf("<ARITHOP, /> (line %d)\n", line_num); char_count += 1; }

";"                 { printf("<DELIM, ;> (line %d)\n", line_num); char_count += 1; }
","                 { printf("<DELIM, ,> (line %d)\n", line_num); char_count += 1; }
"("                 { printf("<DELIM, (> (line %d)\n", line_num); char_count += 1; }
")"                 { printf("<DELIM, )> (line %d)\n", line_num); char_count += 1; }
"{"                 { printf("<DELIM, {> (line %d)\n", line_num); char_count += 1; }
"}"                 { printf("<DELIM, }> (line %d)\n", line_num); char_count += 1; }

{id}                { printf("<ID, \"%s\"> (line %d)\n", yytext, line_num); char_count += yyleng; word_count++; }
{number}            { printf("<NUM, %s> (line %d)\n", yytext, line_num); char_count += yyleng; word_count++; }

\"([^"\\]|\\.)*\"   { printf("<STRING, %s> (line %d)\n", yytext, line_num); char_count += yyleng; }

.                   { printf("LEXICAL ERROR: Unrecognized character '%s' at line %d\n", yytext, line_num); char_count++; }

%%

int yywrap() {
    return 1;
}

int main(int argc, char **argv) {
    printf("--- Scanning Started ---\n");
    yylex();
    printf("--- Scanning Finished ---\n");
    printf("Total Lines: %d, Words: %d, Characters: %d\n", line_num, word_count, char_count);
    return 0;
}
