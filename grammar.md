## Gramatyka

Rule id | Producion
-------|------------
Rule 1 | S' -> stmt_list_opt
Rule 2 | while_stmt -> WHILE expr stmt_list END
Rule 3 | stmt_list -> stmt
Rule 4 | stmt_list -> stmt_list stmt
Rule 5 | stmt -> expr_stmt
Rule 6 | stmt -> if_stmt
Rule 7 | stmt -> while_stmt
Rule 8 | stmt -> BREAK
Rule 9 | stmt -> CONTINUE
Rule 10| stmt -> function_stmt
Rule 11| expr_stmt -> expr SEMI
Rule 12| function_stmt -> FUNCTION ID EQ function_declr stmt_list END
Rule 13| function_declr -> ID LPAREN args_opt RPAREN
Rule 14| args_opt -> <empty>
Rule 15| args_opt -> args
Rule 16| args -> ID
Rule 17| args -> args COMMA ID
Rule 18| stmt_list_opt -> <empty>
Rule 19| stmt_list_opt -> stmt_list
Rule 20| expr -> LPAREN expr RPAREN
Rule 21| expr -> function_call
Rule 22| expr -> ID
Rule 23| expr -> NUMBER
Rule 24| expr -> STRING
Rule 25| expr -> expr1
Rule 26| expr -> expr2
Rule 27| function_call -> ID LPAREN expr_list_opt RPAREN
Rule 28| expr_list_opt -> <empty>
Rule 29| expr_list_opt -> expr_list
Rule 30| expr_list -> expr
Rule 31| expr_list -> expr_list COMMA expr
Rule 32| expr1 -> NEG expr
Rule 33| expr2 -> expr LT expr
Rule 34| expr2 -> expr AND expr
Rule 35| expr2 -> expr DIV expr
Rule 36| expr2 -> expr POW expr
Rule 37| expr2 -> expr GE expr
Rule 38| expr2 -> expr GT expr
Rule 39| expr2 -> expr LE expr
Rule 40| expr2 -> expr MINUS expr
Rule 41| expr2 -> expr MUL expr
Rule 42| expr2 -> expr OR expr
Rule 43| expr2 -> expr PLUS expr
Rule 44| expr2 -> expr EQ expr
Rule 45| expr2 -> expr EQEQ expr
Rule 46| if_stmt -> IF expr stmt_list_opt elseif_stmt END
Rule 47| elseif_stmt -> <empty>
Rule 48| elseif_stmt -> ELSE stmt_list_opt
Rule 49| elseif_stmt -> ELSEIF expr stmt_list_opt elseif_stmt