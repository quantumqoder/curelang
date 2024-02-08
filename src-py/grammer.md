expr : term ((PLUS | MINUS) term)*
term : factor ((MULTIPLY | DIVIDE) factor)*
factor: NUMBER
      : (PLUS|MINUS) factor
      : LPAREN expr RPAREN