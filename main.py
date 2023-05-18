import pygame
import math
import pygame_widgets
from pygame_widgets.slider import Slider

largura, altura = 800, 600  # definir a largura e a altura da janela
Out = False
Acd = False
comprimento = 0  # o comprimento entre a bola e o suporte
angulo = 0
vel = 0  # velocidade
Acc_angular = 0  # aceleração

# START
pygame.init()
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Pendulo')
clock = pygame.time.Clock()
texto_font = pygame.font.Font(None, 20)
texto_1 = texto_font.render('Gravidade', False, (255, 255, 255))
texto_2 = texto_font.render('Resistencia', False, (255, 255, 255))
slider_Gravidade = Slider(screen, 10, 45, 60, 5, min=0, max=100, step=1, initial=20)
slider_Resistencia = Slider(screen, 10, 95, 60, 5, min=1, max=100, step=1, initial=96)
texto_angulo = texto_font.render(str(angulo), False, (255, 255, 255))


class Bola(object):

    def __init__(self, x_y, raio) -> None:  # Definir coordenadas da bola e do raio
        self.x = x_y[0]
        self.y = x_y[1]
        self.raio = raio

    def draw(self, screen_local) -> None:  # Desenhar círculo e linha com base em coordenadas XY
        pygame.draw.lines(screen_local, (0, 0, 250), False, [(largura / 2, 50), (self.x, self.y)], 2)
        pygame.draw.circle(screen_local, (250, 250, 250), (self.x, self.y), self.raio)
        pygame.draw.circle(screen_local, (0, 0, 250), (self.x, self.y), self.raio - 2)
        screen_local.blit(texto_1, (10, 30))
        screen_local.blit(texto_2, (10, 80))
        screen_local.blit(texto_angulo, (410, 25))
        pygame_widgets.update(pygame.event.get())
        pygame.display.update()


def angulo_comprimento() -> tuple:  # Envie de volta o comprimento e o ângulo no primeiro clique na tela
    comprimento_local = math.sqrt(((pendulo.x - largura / 2) ** 2) + ((pendulo.y - 50) ** 2))
    angulo_local = math.asin((pendulo.x - largura / 2) / comprimento_local)
    return angulo_local, comprimento_local


def comprimento_posicao(comprimento_local: float, angulo_local: float) -> None:
    # com ângulo e comprimento calcular posição x e y
    pendulo.x = round(largura / 2 + comprimento_local * math.sin(angulo_local))
    pendulo.y = round(50 + comprimento_local * math.cos(angulo_local))


def repor() -> None:  # Limpe a tela e inicie uma nova grade e um novo quadro de pêndulo com novas coordenadas
    screen.fill((0, 0, 0))
    pendulo.draw(screen)
    pygame.display.update()


pendulo = Bola((int(largura / 2), largura / 2), 15)  # Coordenadas aleatoria

while not Out:

    clock.tick(60)  # Fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Out = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x >= 80:
                pendulo = Bola(pygame.mouse.get_pos(), 15)
                angulo, comprimento = angulo_comprimento()
                Acd = True
                vel = 0
                Acc_angular = 0  # aceleração
            angulo_degrees = round(math.degrees(angulo), 1)
            if angulo_degrees < 0:
                angulo_degrees = 360 + angulo_degrees
            texto_angulo = texto_font.render(str(angulo_degrees), False, (255, 255, 255))

        if event.type == pygame.KEYDOWN:
            Acd = False
        if event.type == pygame.KEYUP:
            Acd = True
        # Acd = event.type == pygame.KEYUP

    if Acd:  # Aumente a aceleração e o resistencia no movimento do pêndulo
        Acc_angular = ((-slider_Gravidade.value/10) / comprimento) * math.sin(angulo)
        vel += Acc_angular
        vel *= (slider_Resistencia.value * 0.001) + 0.9  # Empuxo
        angulo += vel
        comprimento_posicao(comprimento, angulo)

    repor()

pygame.quit()
