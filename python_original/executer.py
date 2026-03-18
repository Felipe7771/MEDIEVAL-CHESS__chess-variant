import config.menu as menu
menu.setIncialMenu()
#=========================================================================
#=========================================================================
# !BEM VINDO USUÁRIO AO XADREZ PYTHON!
#=========================================================================
# ? Para iniciar o jogo, apenas inicialize este aquivo (em VScode: Ctrl+F5)

# Neste projeto, você poderá jogar um jogo de xadrez dinâmico com duas pessoas para jogar.
# Ao iniciar, você pode inserir o nome de cada jogador para indentificar melhor a vez de jogar devido a possíveis mudanças de cores atrelados ao tema de cor do ambiente em execução

# Com as brancas começando, você pode escolher qual peça jogar alterando a seleção (sempre começa selecionando o REI) com o WASD ou as setas, clicando em ESPAÇO você seleciona a peça para se mover.
# Será exibido no campo indicadores de movimentos que a peça pode fazer, sendo:

# Peão   -> Move para frente 1 bloco e ataca na diagonal;
#             Inicio do Jogo pode mover 2 blocos
#               Chegada no fim do tabuleiro recebe transformação para (rainha, torre, bispo e cavalo)
# Torre  -> Move vertical e horizontal livremente
# Bispo  -> Move diagonal livremente
# Cavalo -> Pula em L (dois espaços retos e um para o lado)
# Rainha -> Move diagonal, vertical e horizontal livremente
# Rei    -> Move 1 espaço para qualquer lado

# escolhendo também com WASD e setas, pressione ENTER para executar o movimento e passar a vez ao adversário 

# Vence o jogo APENAS se o Rei do adversário está sendo atacado (XEQUE) e nenhum movimento possível que o adversário possa fazer tanto com o rei quanto com suas outras peças possa tirá-lo de ser atacado, o famoso XEQUE-MATE.
# Com isso, durante o jogo, será impossibilitado o jogador realizar o movimento que deixe o rei em xeque, conhecido como movimento ilegal, assim, o jogo vai retornar seu movimento para que você poss jogar outra peça ou movimento válido.

# Durante a jogatina, após a realização de uma jogada, o jogo irá avaliar a jogada feita e tentar exibir a melhor avaliação para o jogador, sendo exibido com os símbolos ao lado do tabuleiro dessa forma: (símbolo) SIGNIFICADO 
# ! O sistema TENTA entender o que sua jogada significa no jogo, para a decisão, alguns resultados possuem mais pesos que outras, na hora da avaliação, o jogo exibirá a análise de maior peso, ou seja, apesar de ser exibido apenas um símbolo, as jogadas podem ter mais de uma única análise, o jogo está apenas selecionando a "mais provável" de ter sido.