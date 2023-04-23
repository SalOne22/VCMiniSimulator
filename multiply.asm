def a 10
def b 5
def one 1

; multiply a and b
lda a
sta 0
loop:
  lda b
  sub one
  sta b
  jz end
  lda 0
  add a
  sta 0
  jmp loop
end:
  lda 0
  out
  hlt