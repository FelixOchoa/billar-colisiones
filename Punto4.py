import pygame
import math

# Constantes
RADIO_BOLAS = 20
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVEDAD = 9.81
PERDIDA_VELOCIDAD_PARED = 0.50
PERDIDA_VELOCIDAD = 5
VELOCIDAD_INICIAL = 0

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

pygame.font.init()
# Definir la fuente para el texto
fuente = pygame.font.SysFont(None, 25)

# Definir el input box
input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 10, 200, 20)
texto_input = ""

# Definir el botón
boton_golpear = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 50)
texto_boton = 'Golpear!'

# Clases
class Bola:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
    
    def colisionar_mesa(self, ancho, alto):
        if self.x - RADIO_BOLAS < 0:
            self.vx = abs(self.vx) * PERDIDA_VELOCIDAD_PARED
            self.x = RADIO_BOLAS
        elif self.x + RADIO_BOLAS > ancho:
            self.vx = -abs(self.vx) * PERDIDA_VELOCIDAD_PARED
            self.x = ancho - RADIO_BOLAS
        if self.y - RADIO_BOLAS < 0:
            self.vy = abs(self.vy) * PERDIDA_VELOCIDAD_PARED
            self.y = RADIO_BOLAS
        elif self.y + RADIO_BOLAS > alto:
            self.vy = -abs(self.vy) * PERDIDA_VELOCIDAD_PARED
            self.y = alto - RADIO_BOLAS

    
    def perder_velocidad(self, dt):
        if self.vx != 0:
            self.vx -= self.vx/abs(self.vx) * PERDIDA_VELOCIDAD * dt
        if self.vy != 0:
            self.vy -= self.vy/abs(self.vy) * PERDIDA_VELOCIDAD * dt

        # Verificar si la velocidad es muy pequeña y ponerla en cero
        if abs(self.vx) < 0.1:
            self.vx = 0
        if abs(self.vy) < 0.1:
            self.vy = 0


    def dibujar(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), RADIO_BOLAS)

    def colisionar(self, otra_bola):
        dx = self.x - otra_bola.x
        dy = self.y - otra_bola.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist < RADIO_BOLAS:
            overlap = RADIO_BOLAS - dist
            angle = math.atan2(dy, dx)
            sin_a = math.sin(angle)
            cos_a = math.cos(angle)

            # mover las bolas para que ya no se superpongan
            self.x += overlap * cos_a / 2
            self.y += overlap * sin_a / 2
            otra_bola.x -= overlap * cos_a / 2
            otra_bola.y -= overlap * sin_a / 2

            # calcular las nuevas velocidades
            (self.vx, self.vy) = (cos_a*self.vx + sin_a*self.vy,
                                cos_a*otra_bola.vx + sin_a*otra_bola.vy)
            (otra_bola.vx, otra_bola.vy) = (cos_a*otra_bola.vx - sin_a*self.vy,
                                            cos_a*self.vx - sin_a*otra_bola.vy)

            v1f = ((self.vx**2 + self.vy**2)**0.5)
            v2f = ((otra_bola.vx**2 + otra_bola.vy**2)**0.5)

            v1theta = math.atan2(self.vy, self.vx)
            v2theta = math.atan2(otra_bola.vy, otra_bola.vx)

            (self.vx, self.vy) = (v2f*math.cos(v2theta), v2f*math.sin(v2theta))
            (otra_bola.vx, otra_bola.vy) = (v1f*math.cos(v1theta), v1f*math.sin(v1theta))


    def mover(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

        self.colisionar_mesa(WIDTH, HEIGHT)

        if self.x - RADIO_BOLAS < 0 or self.x + RADIO_BOLAS > WIDTH:
            self.vx = -self.vx

        if self.y - RADIO_BOLAS < 0 or self.y + RADIO_BOLAS > HEIGHT:
            self.vy = -self.vy

class Mesa:

    def __init__(self):
        self.bolas = []


    def simular(self, dt):
        for i in range(len(self.bolas)):
            
            bola = self.bolas[i]
            bola.perder_velocidad(dt)
            bola.mover(dt)

            for j in range(i+1, len(self.bolas)):
                otra_bola = self.bolas[j]
                bola.colisionar(otra_bola)

    def dibujar(self, surface):
        surface.fill(VERDE)

        for bola in self.bolas:
            bola.dibujar(surface)



# Función principal
def main():
    pygame.init()
    pygame.font.init()
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulación de billar")

    mesa = Mesa()
    
    bolas = [
        Bola(400, 193, 0, 0, ROJO),
        Bola(370, 150, 0, 0, AZUL),
        Bola(400, 500, 0, -200, BLANCO),
        Bola(430, 150, 0, 0, NEGRO),
    ]

    mesa.bolas = bolas
    reloj = pygame.time.Clock()

    while True:
        dt = reloj.tick(FPS) / 1000.0

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Lógica
        mesa.simular(dt)
        for bola in bolas:
            bola.perder_velocidad(dt)

        # Dibujar
        mesa.dibujar(pantalla)
        pygame.display.flip()

if __name__ == '__main__':
    main()

