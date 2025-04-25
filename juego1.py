import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 500, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Gallina")

# Colores
rojo = (255, 0, 0)
azul = (0, 0, 255)
verde = (0,255,0)
rosado = (255,195,203)
negro = (0,0,0)
amarillo = (255,255,0)
blanco = (255,255,255)
naranja = (255,165,0)
cian = (0,255,255)
marron = (128, 0, 0)
gris = (128, 128, 128)
gris_os = (51,47,44)
amarillo_pas = (253,253,150)
rojo_claro = (255,105,97)

# Clase Gallina
class Gallina(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(amarillo)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)

    def mover(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 10
        if keys[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += 10
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += 10

    def reiniciar(self):
        self.rect.center = (ANCHO // 2, ALTO - 50)

# Clase Vehículo
class Vehiculo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = pygame.Surface((80, 40))
        self.image.fill(azul)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = velocidad

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.right < 0:  # Sale por la izquierda
            self.rect.left = ANCHO
        elif self.rect.left > ANCHO:  # Sale por la derecha
            self.rect.right = 0

# Función para dibujar casas decorativas
def dibujar_casas(pantalla):
    for i in range(1):
        x = ANCHO - 130
        y = 50 + i * 180
        
           # Casas arriba (Cuadrado)
        pygame.draw.rect(pantalla,rojo_claro,((50, 50),(80, 80)),100)
        pygame.draw.rect(pantalla,rojo_claro,((200, 50),(80, 80)),100)
        pygame.draw.rect(pantalla,rojo_claro,((350, 50),(80, 80)),100)
        # Casas abajo (Cuadrado)
        pygame.draw.rect(pantalla,rojo_claro,((50, 520),(80, 80)),100)
        pygame.draw.rect(pantalla,rojo_claro,((350, 520),(80, 80)),100)
        # Casa arriba (Techo)
        pygame.draw.rect(pantalla, naranja, ((40,40), (100,30)), 100)
        pygame.draw.rect(pantalla, naranja, ((190,40), (100,30)), 100)
        pygame.draw.rect(pantalla, naranja, ((340,40), (100,30)), 100)
        # Casas abajo (Techo)
        pygame.draw.rect(pantalla, naranja, ((40,510), (100,30)), 100)
        pygame.draw.rect(pantalla, naranja, ((340,510), (100,30)), 100)

# Configuración inicial del juego
gallina = Gallina()
vehiculos = pygame.sprite.Group()

for i in range(5):
    y = 200 + i * 60
    x = random.randint(0, ANCHO)
    velocidad = random.choice([-5, 5])
    vehiculo = Vehiculo(x, y, velocidad)
    vehiculos.add(vehiculo)

todos_sprites = pygame.sprite.Group()
todos_sprites.add(gallina)
todos_sprites.add(vehiculos)

# Variables del juego
reloj = pygame.time.Clock()
puntuacion = 0
vidas = 3
ejecutando = True
colision_detectada = False

# Bucle principal del juego
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Capturar teclas presionadas
    teclas = pygame.key.get_pressed()
    gallina.mover(teclas)

    # Actualizar posiciones de los vehículos
    vehiculos.update()

    # Verificar colisión de la gallina con los vehículos
    if pygame.sprite.spritecollideany(gallina, vehiculos) and not colision_detectada:
        colision_detectada = True
        print("¡La gallina fue golpeada!")
        vidas -= 1
        if vidas == 0:
            print("¡Juego terminado! La gallina se quedó sin vidas.")
            ejecutando = False  # Finalizar el juego
        gallina.reiniciar()
        puntuacion = 0  # Reiniciar la puntuación
    elif not pygame.sprite.spritecollideany(gallina, vehiculos):
        colision_detectada = False

    # Verificar si la gallina llegó al otro lado
    if gallina.rect.top <= 0:
        puntuacion += 1
        print(f"¡Puntuación: {puntuacion}!")
        gallina.reiniciar()

    # Dibujar en pantalla
    pantalla.fill(verde)
    pygame.draw.rect(pantalla, gris, (0, 200, ANCHO, 300))
    dibujar_casas(pantalla)
    todos_sprites.draw(pantalla)

    # Dibujar texto de puntuación y vidas
    fuente = pygame.font.SysFont(None, 36)
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, blanco)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, blanco)
    pantalla.blit(texto_puntuacion, (10, 10))
    pantalla.blit(texto_vidas, (10, 50))

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
