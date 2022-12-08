import PySimpleGUI as sg


#  porta = "COM10"
#  velocidade = 9600
#  conecao = serial.Serial (porta, velocidade)

sg.theme('DarkBlue2')
# DarkBrown7 PythonPlus SandyBeach
# MODO PROGRAMAÇÃO-------------------------------------------------------------------------------------------------------

def separaEquacao(linha, LED, MEMORIA):
    lista = []
    lista[:] = formatacao(linha)
    aux=0
    aux2 = 0
    divisoria = lista.index('=')
    if 'l' in lista[:divisoria]:
        aux = lista[lista.index('l')+1]
        aux = 'l' + str(aux)
        aux2 = LED.index(aux)+2
        LED[aux2] = lista[divisoria:]
        return LED
    aux=0
    aux2 = 0
    if 'm' in lista[:divisoria]:
        aux = lista.index('m')
        aux3 = lista[lista.index('m')+1]
        if (divisoria!=2):
            aux = aux+1
            print(lista[aux])
            lista[aux] = lista[aux]+lista[aux+1]
            lista.pop(aux+1)
        aux3 = 'm' + str(aux3)
        aux2 = MEMORIA.index(aux3)+2
        MEMORIA[aux2] = lista[divisoria:]
        return MEMORIA
    return "Invalido"




def organizaMemoria(expressao):
    has = True
    i = 0
    isNumber = 0
    j=1
    while has:
        if 'm' in expressao[i:]:
            aux = expressao.index('m', i)
            while j < 10:
                if expressao[aux+2] == j:
                    isNumber = isNumber+1
                if isNumber != 0:
                    aux = aux+1
                    expressao[aux] = expressao[aux]+expressao[aux+1]
                    expressao.pop(aux+1)
                j = j+1
        else:
            has = False
        i = i+1
    return expressao

def formatacao(expressao):
    if (expressao == ''):
        return "expressao"
    else:
        lista = []
        lista[:] = expressao
        lista = [j for j in lista if j.strip()]
        lista = organizaMemoria(lista)
        return lista

def opAnd(a, b):
    if (a and b):
        return True
    else:
        return False


def opOr(a, b):
    if (a or b):
        return True
    else:
        return False


def opNot(a):
    if (a):
        return False
    else:
        return True

def entreParenteses(expressao, fim, inicio, BTN, LED, MEMORIA):
    #print("\n\n\n\nentro função")
    a = False
    b = False
    hasAnd = True
    hasOr = True
    cabo = False
    notUnico = False
    unico = False
    i = inicio
    final = fim
    inicioOp = inicio+1
   #print(
   #     "\n\n\n\ninicio = (expressao[inicio:fim])"+str(expressao[inicio:fim]))
    # conferir conteudo ja checado o valor
  # Checar Memoria
    if 'm' in expressao[i:fim]:
        aux = expressao[expressao.index('m', i)+1]
        print(aux)
        aux = 'm' + aux
      #  print("+3 " + str(MEMORIA[MEMORIA.index(aux)+3]))
     #   print("+2 " + str(MEMORIA[MEMORIA.index(aux)+2]))
    #    print("+1 " + str(MEMORIA[MEMORIA.index(aux)+1]))
   #     print("0 " + str(MEMORIA[MEMORIA.index(aux)]))
        if ('expressao') in MEMORIA[MEMORIA.index(aux)+2]:
            return False
 #       # Checar LED
    if 'l' in expressao[i:fim]:
        aux = expressao[expressao.index('l', i)+1]
        aux = 'l' + aux
        if ('expressao') in LED[LED.index(aux)+2]:
            return False

    if not ('+' in expressao[inicio:fim]):
        hasOr = False
    if not ('*' in expressao[inicio:fim]):
        hasAnd = False

    if not ('+' in expressao[inicio:fim]) and not ('*' in expressao[inicio:fim]):
  #      print("entrou")
        auxIndex = inicio
        if expressao[auxIndex+1] == "!":
            notUnico = True
            auxIndex = auxIndex+1
        if expressao[auxIndex+1] == True or expressao[auxIndex+1] == False:
            auxBool = expressao[auxIndex+1]
        elif expressao[auxIndex+1] == 'm':
            aux = 'm' + expressao[auxIndex+2]
            auxBool = MEMORIA[MEMORIA.index(aux)+1]
 #           print(str(auxBool))
        elif expressao[auxIndex+1] == 'l':
#
            aux = 'l' + expressao[auxIndex+2]
            auxBool = LED[LED.index(aux)+1]
        elif expressao[auxIndex+1] == 'b':
            auxBool = BTN[int(expressao[auxIndex+2])-1]

        if (notUnico):
            auxBool = opNot(auxBool)
        expressao[inicioOp] = auxBool
        if (expressao[inicio-1]) == '!':
            expressao[inicioOp] = opNot(expressao[inicioOp])
        return expressao[inicioOp]
        

    while hasAnd == True or hasOr == True:
        #
        auxIndex = 0
        operacao = 0
        if ('+' in expressao[inicio:final] and ('*' in expressao[inicio:final])):
            if (expressao.index('*') < expressao.index('+')):
                auxIndex = expressao.index('*')
                operacao = 1
                #i = expressao.index('*', i)
            if (expressao.index('*') > expressao.index('+')):
                auxIndex = expressao.index('+')
                operacao = 2
                #i = expressao.index('+', i)
        elif ('+' in expressao[inicio:final]):
         #   print("entrou")
            auxIndex = expressao.index('+')
            operacao = 2
            #i = expressao.index('+', i)
        elif ('*' in expressao[inicio:final]):
            auxIndex = expressao.index('*')
            operacao = 1
                #i = expressao.index('*', i)
        if (operacao != 0):
        #    print("\n\n\nentrou operação")
            # not na frente
            finalOp = auxIndex+3

            inicioOp = auxIndex-2
            if (expressao[inicioOp] == '('):
                inicioOp = inicioOp+1
            if expressao[auxIndex+1] == "!":
                finalOp = finalOp + 1
                if expressao[auxIndex+2] == True or expressao[auxIndex+2] == False:
                    b = expressao[auxIndex+2]
                elif expressao[auxIndex+2] == 'm':
                    aux = 'm' + expressao[auxIndex+3]
                    b = MEMORIA[MEMORIA.index(aux)+1]
                elif expressao[auxIndex+2] == 'l':
                    aux = 'l' + expressao[auxIndex+3]
                    b = LED[LED.index(aux)+1]
                elif expressao[auxIndex+2] == 'b':
                    b = BTN[int(expressao[auxIndex+3])-1]
                b = opNot(b)
            # sem not na frente
            elif expressao[auxIndex+1] == True or expressao[auxIndex+1] == False:
                b = expressao[auxIndex+1]
            elif expressao[auxIndex+1] == 'm':
                aux = 'm' + expressao[auxIndex+2]
                b = MEMORIA[MEMORIA.index(aux)+1]
            elif expressao[auxIndex+1] == 'l':
                aux = 'l' + expressao[auxIndex+2]
                b = LED[LED.index(aux)+1]
            elif expressao[auxIndex+1] == 'b':
                b = BTN[int(expressao[auxIndex+2])-1]

            # checar o que vem antes
           # print("check")
            if expressao[auxIndex-1] == True or expressao[auxIndex-1] == False:
                a = expressao[auxIndex-1]

            elif expressao[auxIndex-2] == 'm':
                aux = 'm' + expressao[auxIndex-1]
                a = MEMORIA[MEMORIA.index(aux)+1]
            elif expressao[auxIndex-1] == 'l':
                aux = 'l' + expressao[auxIndex-2]
                a = LED[LED.index(aux)+1]
            elif expressao[auxIndex-2] == 'b':
                a = BTN[int(expressao[auxIndex-1])-1]
            if expressao[auxIndex-3] == '!':
                inicioOp = inicioOp-1
                a = opNot(a)
            if (operacao == 1):
                auxBool = opAnd(a, b)
          #      print(auxBool)
            if (operacao == 2):
                auxBool = opOr(a, b)
     #           print(auxBool)
            expressao[inicioOp] = auxBool
            del expressao[(inicioOp+1):finalOp]

        if not ('+' in expressao[inicio:final]):
            hasOr = False
        if not ('*' in expressao[inicio:final]):
            hasAnd = False
        i = i + 1
    if (expressao[inicio-1]) == '!':
        expressao[inicioOp] = opNot(expressao[inicioOp])
   # print("teste")
    return expressao[inicioOp]
def valorExpressao(expressao, BTN, LED, MEMORIA):
    if not 'expressao' in expressao:
        inicio = 0
        fim = 0


        inicio = expressao.index('(')
        fim = expressao.index(')')+1
        auxBool = entreParenteses(expressao, fim, inicio, BTN, LED, MEMORIA)
        expressao[inicio] = auxBool
        del expressao[(inicio+1):fim]      
        return expressao[inicio]
    #


# --------------------------------------------------------------------------------------------------------------------------------
# main
# ============================================================================================================================================================================================================================================

BTN = [False, False, False, False, False, False, False, False]

# front-end -----------------------------------------------------
dados = [
    [sg.Text('=========================================',size=(300, 0))],
    [sg.Text('Text:', size=(15, 0))],
    [sg.Multiline(size=(45, 20),key='mult')],
    [sg.Text('Digite somente o nome do arquivo', size=(25, 0))],
    [sg.Text('Filename', size=(7, 0)),sg.Input(size=(22, 1),key='dir'), sg.FileBrowse(size=(10, 1))], 
    [sg.Button('run', size=(15, 0)),sg.Button('Save',size=(10, 0)),sg.Button('Carregar',size=(10, 0))]]
layout = [[sg.Column(dados, size=(350, 500))]]
window = sg.Window('CLP', layout)


while True:
    # declaração
    LED = ['l1', False, "expressao", 'l2', False, "expressao", 'l3', False, "expressao", 'l4', False, "expressao",
           'l5', False, "expressao", 'l6', False, "expressao", 'l7', False, "expressao", 'l8', False, "expressao"]
    MEMORIA = ['m1', False, "expressao", 'm2', False, "expressao", 'm3', False, "expressao",
               'm4', False, "expressao", 'm5', False, "expressao", 'm6', False, "expressao", 'm4', False, "expressao", 'm5', False, "expressao", 'm6', False, "expressao",'m7', False, "expressao", 'm8', False, "expressao", 'm9', False, "expressao",'m10', False, "expressao", 'm11', False, "expressao", 'm12', False, "expressao", 'm13', False, "expressao", 'm14', False, "expressao", 'm15', False, "expressao", 'm16', False, "expressao"]
    # ---------------------------------------------------------------
    # Modo codar
    event, values = window.read()
    if event == 'Carregar':
        diretorio = values['dir']
        arquivo = open(diretorio,'r', encoding="UTF-8")

        for linha in arquivo:
            linha = linha.rstrip()
            window['mult'].print(linha)
        arquivo.close()

    if event == 'Save':
        
        arquivo = open('arq01.txt','w',encoding="UTF-8")
        textField = values['mult']
        print(textField)
        arquivo.write(textField)


    if event == 'run':
        #LED[LED.index('l1')+2] = formatacao(values['l1'])
        
        textField = values['mult']
        #print(textField)
        k=0
        listaAux = textField.split("\n") # sendo text field o que pegou do front
        #print(listaAux)
        for line in listaAux:
            verifica = separaEquacao(listaAux[k], LED, MEMORIA)
            if (verifica == "Invalido"):
                print("Invalido")
            elif (verifica[0] == 'l1'):
                LED = verifica
            elif (verifica[0] == 'm1'):
                MEMORIA = verifica
            k=k+1
        # codig = str(conecao.readline())


        # if codig == 'b1':
        #     if(BTN[0] == True):
        #         BTN[0] = False
        #     else:
        #         BTN[0] = True
        # if codig == 'b2':
        #     if(BTN[1] == True):
        #         BTN[1] = False
        #     else:
        #         BTN[1] = True
        # if codig == 'b3':
        #     if(BTN[2] == True):
        #         BTN[2] = False
        #     else:
        #         BTN[2] = True
        # if codig == 'b4':
        #     if(BTN[3] == True):
        #         BTN[3] = False
        #     else:
        #         BTN[3] = True
        # if codig == 'b5':
        #     if(BTN[4] == True):
        #         BTN[4] = False
        #     else:
        #         BTN[4] = True
        # if codig == 'b6':
        #     if(BTN[5] == True):
        #         BTN[5] = False
        #     else:
        #         BTN[5] = True
        # if codig == 'b7':
        #     if(BTN[6] == True):
        #         BTN[6] = False
        #     else:
        #         BTN[6] = True
        # if codig == 'b8':
        #     if(BTN[7] == True):
        #         BTN[7] = False
        #     else:
        #         BTN[7] = True
        # # # # se campo vasio = []
        # interface info-------------------------------------------------
        # loop modo run
        BTN = [True, False, True, False, True, False, True, False]
        i = 1
        while (i < 17):
            aux = 'm' + str(i)
            if (MEMORIA[MEMORIA.index(aux)+2] != ("expressao")):
                MEMORIA[MEMORIA.index(aux)+1] = valorExpressao(MEMORIA[MEMORIA.index(aux)+2], BTN, LED, MEMORIA)
                print(str(aux) + ":" + str(MEMORIA[MEMORIA.index(aux)+1]))
            if (i < 9):
                aux = 'l' + str(i)
                if (LED[LED.index(aux)+2] != ("expressao")):
                    LED[LED.index(aux)+1] = valorExpressao(LED[LED.index(aux)+2],
                                                        BTN, LED, MEMORIA)
                    # manda info pro arduino aqui mesmo LED(i) = (LED[LED.index(aux)+1])
                    print(str(aux) + ":" + str(LED[LED.index(aux)+1]))
            i = i+1
    # ============================================================================================================================================================================================================================================
    if event == sg.WIN_CLOSED or event == 'Cancel':
        window.close()
        #conecao.close()
        break



# [sg.Text('LED 2:', size=(15, 0)), sg.InputText(size=(40, 1), key='l2')],
    # [sg.Text('LED 3:', size=(15, 0)), sg.InputText(size=(40, 1), key='l3')],
    # [sg.Text('LED 4:', size=(15, 0)), sg.InputText(size=(40, 1), key='l4')],
    # [sg.Text('LED 5:', size=(15, 0)), sg.InputText(size=(40, 1), key='l5')],
    # [sg.Text('LED 6:', size=(15, 0)), sg.InputText(size=(40, 1), key='l6')],
    # [sg.Text('LED 7:', size=(15, 0)), sg.InputText(size=(40, 1), key='l7')],
    # [sg.Text('LED 8:', size=(15, 0)), sg.InputText(size=(40, 1), key='l8')],
    # [sg.Text('================================================= ', size=(300, 0))],
    # [sg.Text('Memória 1:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m1')],
    # [sg.Text('Memória 2:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m2')],
    # [sg.Text('Memória 3:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m3')],
    # [sg.Text('Memória 4:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m4')],
    # [sg.Text('Memória 5:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m5')],
    # [sg.Text('Memória 6:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m6')],
    # [sg.Text('Memória 7:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m7')],
    # [sg.Text('Memória 8:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m8')],
    # [sg.Text('Memória 9:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m9')],
    # [sg.Text('Memória 10:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m10')],
    # [sg.Text('Memória 11:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m11')],
    # [sg.Text('Memória 12:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m12')],
    # [sg.Text('Memória 13:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m13')],
    # [sg.Text('Memória 14:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m14')],
    # [sg.Text('Memória 15:', size=(15, 0)),
    #  sg.InputText(size=(40, 1), key='m15')],
    # [sg.Text('Memória 16:', size=(15, 0)),sg.InputText(size=(40, 1), key='m16')],