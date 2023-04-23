def a 15
def b 7

; load value of variable a into accumulator
lda a

; subtract value of variable b from accumulator
sub b

; store result in variable a
sta a

; output result
out

; halt the CPU
hlt