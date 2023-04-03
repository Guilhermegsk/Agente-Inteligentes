import numpy as np
import random 
from random import randint
import random
import matplotlib.pyplot as plt

global cont
global posX 
global posY 
global lixeira
Pcima = 0
Pbaixo = 1
Pesquerda = 2
Pdireita = 3

#conteudo_vizinho = [0] * 8


global statusLixo 
statusLixo = 0#0 para sem lixo; 1 para com lixo
status = 0 #NoOP
posX = 0 #posição eixo X
posY = 0 #posição eixo y
pontos = [] #array de pontos feitos pelo robo
posicao = [] #array de pontos disponíveis a partir de um local inicial (x,y)

def verificar(ambiente, ordem):
  posicao.clear()
  #print(ambiente[posY, posX])
  y_atual, x_atual = posY, posX
  if Pcima == ordem:
    for i in range(7):
      if y_atual > -1:
        posicao.append(ambiente[y_atual, posX])
        y_atual -= 1
  if Pbaixo == ordem:
    for i in range(7):
      if y_atual<20:
        posicao.append(ambiente[y_atual, posX])
        y_atual += 1
  if Pesquerda == ordem:
    for i in range(7):
      if x_atual>-1:
        posicao.append(ambiente[posY, x_atual])
        x_atual -= 1
  if Pdireita == ordem:
    for i in range(7):
      if x_atual<20:
        posicao.append(ambiente[posY, x_atual])
        x_atual += 1;
  # else:
  #   print("\nEntrada de ordem inválida")
  return posicao

  
def atualizar_estado(ambiente ,acao):
        global statusLixo
        global posY
        global posX
        # Atualiza o estado do ambiente de acordo com a ação executada pelo robô
        if acao == "andar_esquerda":
            if posX>0:
                esquerda(ambiente)
        elif acao == "andar_direita":
            if posX<19:
                direita(ambiente)
        elif acao == "andar_cima":
            if posY > 0:
                cima(ambiente)
        elif acao == "andar_baixo":
            if posY<19:
                baixo(ambiente)
        elif acao == "pegar_lixo":
          if ambiente[posY, posX] == 5:
            pontos.append(ambiente[posY, posX])
            statusLixo = 1
            ambiente[posY, posX] = 0
          elif ambiente[posY, posX] == 1:
            pontos.append(ambiente[posY, posX])
            statusLixo = 1
            ambiente[posY, posX] = 0            
        elif acao == "soltar_lixo":
          print("LIXEIRA : Esta na lixeira" , pontos)
          statusLixo = 0
          posY = 0
          posX = 0
          #andar_para(posY, posX, 0, 0)#retorna pro inicio
            


def preencher_ambiente():
  global lixeira
  cont = 0
  ambiente = np.zeros([20, 20], dtype=int)
  ambiente[19,19] = -1
  lixeira = ambiente[19,19]
  ambiente[5,0] = 5
  ambiente[3, 3] = 5
  ambiente[15, 14] = 5
  ambiente[12, 9] = 5
  ambiente[18, 19] = 5

  ambiente[3,0] = 1
  ambiente[0, 1] = 1
  ambiente[2, 19] = 1
  ambiente[11, 10] = 1
  ambiente[14, 13] = 1
  ambiente[6,5] = 1
  ambiente[9, 9] = 1
  ambiente[16, 17] = 1
  ambiente[13, 2] = 1
  ambiente[19, 18] = 1
  
  #----Gerar aleatório-----
  
  # for j in range(ambiente.shape[0]):
  #   i = randint(1,20)
  #   k = randint(1,20)
  #   if ambiente[i-1, k-1] == 0 :
  #     ambiente[i-1, k-1] = 1
  #     cont = cont+1
  #   else:
  #     i = randint(1,20)
  #     k = randint(1,20)

  # for j in range(ambiente.shape[0]):
  #   i = randint(1,20)
  #   k = randint(1,20)
  #   if ambiente[i-1, k-1] == 0 :
  #     ambiente[i-1, k-1] = 5
  #     cont = cont+1
  #   else:
  #     i = randint(1,20)
  #     k = randint(1,20)

  #print(ambiente)
  return ambiente

#ambiente = preencher_ambiente()


def direita(ambiente):
  global posX
  if posX<=18:
    posX = posX+1
    return posX

def esquerda(ambiente): 
  global posX
  if posX>1:
    posX -= 1
    return posX

def cima(ambiente):
  global posY
  if posY > 1:
    posY -= 1
    return posY

def baixo(ambiente):
  global posY
  if posY<= 18:
    posY += 1
    return posY #ambiente[posY, posX]

def andar_para(posicao_Y, posicao_X, posicao_destinoY, posicao_destinoX):
  y_atual = posicao_Y
  x_atual = posicao_X
  y_destino = posicao_destinoY
  x_destino = posicao_destinoX
  
  for i in range(ambiente.shape[0]):
    #print('DEBUG: VALOR ATUAL: [',ambiente[posY-1, posX-1], "]")
    #print('DEBUG: VALOR DE POSY: [', posY, ']')
    if posY<20:
      if y_atual < y_destino:
        y_atual +=1
        baixo(ambiente)
    if posY>0:
      if y_atual > y_destino:
        y_atual +=1
        cima(ambiente)
    if posX<20:
      if x_atual < x_destino:
        x_atual +=1
        direita(ambiente)
    if posX>0:
      if x_atual > x_destino:
        x_atual +=1
        esquerda(ambiente)
   

class ReativoSimples:
  def __init__(self, ambiente):
    self.ambiente = ambiente
    #self.carrega = [0]
    
  def decidir_acao(self, ambiente, statusLixo):
    #global lixeira
    if statusLixo == 1: # se estiver carregando lixo, vai para a lixeira
      if ambiente[posY, posX] == -1:
        return 'soltar_lixo'
      else:
        #return random.choice(['andar_esquerda', 'andar_direita', 'andar_cima', 'andar_baixo'])
        andar_para(posY, posX, 19, 19)
        #return 'soltar_lixo'
    else:
      if ambiente[posY, posX] == 5:# se houver lixo reciclável na vizinhança, coleta
        return 'pegar_lixo'
      elif ambiente[posY, posX] == 1:
        return 'pegar_lixo'
      elif 5 in verificar(ambiente, 0):
        return 'andar_cima'
      elif 5 in verificar(ambiente, 1):
        return 'andar_baixo'
      elif 5 in verificar(ambiente, 2):
        return 'andar_esquerda'
      elif 5 in verificar(ambiente, 3):
        return 'andar_direita'
      elif 1 in verificar(ambiente, 0):
        return 'andar_cima'
      elif 1 in verificar(ambiente, 1):
        return 'andar_baixo'
      elif 1 in verificar(ambiente, 2):
        return 'andar_esquerda'
      elif 1 in verificar(ambiente, 3):
        return 'andar_direita'
      else:
        return random.choice(['andar_esquerda', 'andar_direita', 'andar_cima', 'andar_baixo'])
      
class AgenteBaseadoEmModelos:
    def __init__(self, estado_inicial):
        self.estado_atual = estado_inicial
        

    def decidir_acao(self, ambiente, statusLixo):
        global utilidade
        utilidade = 0
        acoes_possiveis = ['andar_esquerda', 'andar_direita', 'andar_cima', 'andar_baixo', 'pegar_lixo', 'soltar_lixo', 'NoOp']
        
        if statusLixo == 1: # se estiver carregando lixo, vai para a lixeira
          if ambiente[posY, posX] == -1:
            return 'soltar_lixo'
          else:
            andar_para(posY, posX, 19, 19)
            return 'soltar_lixo'

        # inicializa com ação NoOp
        melhor_acao = 'NoOp'
        verificar(ambiente, i)
        melhor_utilidade = 0 #self.avaliar_estado(self.estado_atual)

        # simula as possíveis consequências de cada ação e escolhe a ação com a melhor utilidade
        for acao in acoes_possiveis:
          if acao == 'andar_esquerda':
          #estado_futuro = atualizar_estado(ambiente , acao)
            utilidade = self.avaliar_estado(verificar(ambiente, 2))
          elif acao == 'andar_direita':
            utilidade = self.avaliar_estado(verificar(ambiente, 3))
          elif acao == 'andar_cima':
            utilidade = self.avaliar_estado(verificar(ambiente, 0))
          elif acao == 'andar_baixo':
            utilidade = self.avaliar_estado(verificar(ambiente, 1))
          elif acao == 'pegar_lixo':
            if ambiente[posY, posX] == 5 or ambiente[posY, posX] == 1:
              return 'pegar_lixo'
          elif acao == 'soltar_lixo':
            if ambiente[posY, posX]==-1:
              return 'soltar_lixo'
          if utilidade > melhor_utilidade:
            melhor_acao = acao
            melhor_utilidade = utilidade

        # atualiza estado atual do agente
        #self.estado_atual = atualizar_estado(ambiente, melhor_acao)
        if melhor_utilidade == 0:
          return random.choice(['andar_esquerda', 'andar_direita', 'andar_cima', 'andar_baixo'])
        return melhor_acao

    def avaliar_estado(self, posicao):
        global utilidade
        #x_agente, y_agente, carregando, lixos, lixeira = estado

        # calcula a utilidade do estado como a soma dos valores dos lixos presentes no ambiente
        if 5 in posicao:
          utilidade += 5
        if 1 in posicao:
          utilidade +=1

        return utilidade  
      
      
def exibir():
    global posX
    global posY

    # Altera o esquema de cores do ambiente
    plt.imshow(ambiente, 'gray')
    plt.nipy_spectral()

    # Coloca o agente no ambiente 
    plt.plot([posX], [posY], marker='o', color='r', ls='')
    plt.show(block=False)

    # Pausa a execução do código por 0.5 segundos para facilitar a visualização
    plt.pause(1)
    plt.clf()   


ambiente = preencher_ambiente()
print(ambiente)
agent = ReativoSimples(ambiente)
agent2 = AgenteBaseadoEmModelos(ambiente)
for i in range(10000):
  atualizar_estado(ambiente, agent.decidir_acao(ambiente, statusLixo))
  #atualizar_estado(ambiente, agent2.decidir_acao(ambiente, statusLixo))
  exibir()
print(pontos)
#print("\n\n", ambiente)
