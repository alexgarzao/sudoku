# sudoku

Ideias básicas:
* Matriz 9x9
* Uma matriz auxiliar de 9x9 onde cada posição contém os possíveis números daquela posição
* Algoritmo recebe o input inicial e mostra o passo-a-passo até resolver tudo
* Pode receber o resultado esperado também para podermos validar se o algoritmo está ok

Como definir o número em cada posição:
* Se só tem uma possibilidade, então está resolvido
* Se só falta um número em uma linha ou coluna, está resolvido
* Se só falta um número em um agrupamento, está resolvido

Algoritmo para chegar a solução (quando não tem necessidade de tentativa e erro):
* Cria a matriz com os resultados (9x9)
* Cria a matriz onde vão ficar os possveis números (9x9x9)
* Baseado no input inicial, popula a matriz de possíveis números com os números conhecidos
* Ajusta a matriz de possibilidades conforme o input inicial
* Fica no laço abaixo:
  * Se em alguma posição só ficou uma possibilidade, está resolvido esta posição. Tenta novamente.
  * Se em alguma linha só falta um número, está resolvida esta posição. Tenta novamente.
  * Se em alguma coluna só falta um número, está resolvida esta posição. Tenta novamente.
  * Se em algum agrupamento só falta um número, está resolvida esta posição. Tenta novamente.
  * Se todos os números foram resolvidos, finish!
  * Se algo foi alterado nesta iteração, vai para o início do laço
  * Se nada mudou nesta iteração, sudoku sem resposta com este algoritmo :-/
