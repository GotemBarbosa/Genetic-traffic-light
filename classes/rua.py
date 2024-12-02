import pygame


class Rua:
    def __init__(self, x, y, largura, altura, orientacao, interseccao=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.orientacao = orientacao
        
        self.carros_esperando = 0
        self.carros_transitando = 0
        self.semaforos = [] #Semaforos que serao adicionados pela classe interconexao
        self.carros = [] #Carros que serao adicionados pela classe carro

        self.interseccao = interseccao  # Ponto de interseção (x, y) se houver
        

    def desenhar_rua(self, tela, interconexoes_area):
        # Define as cores
        cor_rua = (50, 50, 50)          # Cinza para a rua
        cor_borda = (255, 255, 255)    # Branco para a borda
        cor_linha = (255, 255, 255)    # Branco para as linhas de trânsito
        
        # Desenha a rua principal
        pygame.draw.rect(tela, cor_rua, (self.x, self.y, self.largura, self.altura))
        
        # Desenha a borda branca ao redor da rua
        pygame.draw.rect(tela, cor_borda, (self.x, self.y, self.largura, self.altura), 2)
        
        # Desenhar linhas brancas na rua
        if self.orientacao == 'horizontal':
            for i in range(self.x, self.x + self.largura, 70):
                linha = pygame.Rect(i, self.y + self.altura // 2 - 1, 20, 2)
                # Verifica se a linha está dentro de alguma interconexão ou interseção
                pular_linha = False
                if self.interseccao:
                    ix, iy = self.interseccao
                    if ix - self.largura // 2 <= i <= ix + self.largura // 2:
                        pular_linha = True
                if any(inter_area.colliderect(linha) for inter_area in interconexoes_area):
                    pular_linha = True
                if not pular_linha:
                    pygame.draw.line(tela, cor_linha,
                                    (i, self.y + self.altura // 2),
                                    (i + 20, self.y + self.altura // 2), 2)
        elif self.orientacao == 'vertical':
            for i in range(self.y, self.y + self.altura, 40):
                linha = pygame.Rect(self.x + self.largura // 2 - 1, i, 2, 20)
                # Verifica se a linha está dentro de alguma interconexão ou interseção
                pular_linha = False
                if self.interseccao:
                    ix, iy = self.interseccao
                    if iy - self.altura // 2 <= i <= iy + self.altura // 2:
                        pular_linha = True
                if any(inter_area.colliderect(linha) for inter_area in interconexoes_area):
                    pular_linha = True
                if not pular_linha:
                    pygame.draw.line(tela, cor_linha,
                                    (self.x + self.largura // 2, i),
                                    (self.x + self.largura // 2, i + 20), 2)
    
    def atualizar_estatisticas(self):
        self.carros_esperando = 0
        for semaforo in self.semaforos:
            self.carros_esperando += semaforo.carros_esperando