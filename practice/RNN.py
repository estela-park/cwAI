## BBTT: Backpropagation through time, a gradient-based technique for training certain RNN
## https://www.youtube.com/playlist?list=PLoRl3Ht4JOcdU872GhiYWf6jwrk_SNhz9
# RNN을 시간에 대해 펼치면 t개의 FFNN으로 생각할 수 있다.
# 이 때 모든 layer는 같은 recurrent edge로 부터 온 것이기 때문에 동일 param을 공유한다.
# t개의 derivative error를 구하고 동일 위치에 해당하는 G를 평균내어 구하고 업데이트한다.
# 이 때 역전파는 t -> 1 방향으로 갈 때 vanishes, Hessian Optimization으로 해결한다
## https://davi06000.tistory.com/92 -수식

## RNN is usually used to deal with sequencial data x(t),
# which is denoted as x(t)= x(1), . . . , x(τ)