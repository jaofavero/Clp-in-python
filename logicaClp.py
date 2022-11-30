# MODO PROGRAMAÇÃO-------------------------------------------------------------------------------------------------------
def formatacao(expressao):
    lista = []
    lista[:] = expressao
    lista = [j for j in lista if j.strip()]
    return lista


def acharNivel(expressao):
    maiorNivel = 0
    nivel = 0
    i = 0
    hasAbre = True
    hasFecha = True
    if (not ('(' in expressao[i:]) or not (')' in expressao[i:])):
        hasAbre = False
        hasFecha = False
        maiorNivel = -1
    while hasAbre or hasFecha:
        if ('(' in expressao[i:] and ')' in expressao[i:]):
            if (expressao.index('(', i) < expressao.index(')', i)):
                nivel = nivel + 1
                if (maiorNivel < nivel):
                    maiorNivel = nivel
                i = expressao.index('(', i)
            if (expressao.index('(', i) > expressao.index(')', i)):
                nivel = nivel - 1
                i = expressao.index(')', i)
        else:
            hasAbre = False
            if ')' in expressao[i:]:
                nivel = nivel-1
                i = expressao.index(')', i)
            else:
                hasFecha = False
        i = i+1
    if (nivel != 0):
        maiorNivel = -1
    return maiorNivel
# --------------------------------------------------------------------------------------------------------------------------------
# MODO RUN------------------------------------------------------------------------------------------------------------------------


def organizaButton(expressao):
    has = True
    i = 0
    while has:
        if 'b' in expressao:
            aux = expressao.index('b', i)
            expressao[aux] = expressao[aux]+expressao[aux+1]
            expressao.pop(aux+1)
        else:
            has = False
        i = i+1
    return expressao


def organizaLed(expressao):
    has = True
    i = 0
    while has:
        if 'l' in expressao:
            aux = expressao.index('l', i)
            expressao[aux] = expressao[aux]+expressao[aux+1]
            expressao.pop(aux+1)
        else:
            has = False
        i = i+1
    return expressao


def organizaMemoria(expressao):
    has = True
    i = 0
    while has:
        if 'm' in expressao:
            aux = expressao.index('m', i)
            expressao[aux] = expressao[aux]+expressao[aux+1]
            expressao.pop(aux+1)
        else:
            has = False
        i = i+1
    return expressao

# Operadores


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

# fim operadores


def entreParenteses(expressao, fim, inicio, BTN, LED, MEMORIA):
    a = False
    b = False
    hasAnd = True
    hasOr = True
    cabo = False
    i = inicio
    # conferir conteudo ja checado o valor
    # Checar Memoria
    if 'm' in expressao[i:fim]:
        aux = expressao[expressao.index('m', i)+1]
        aux = 'm' + aux
        if not ':' in MEMORIA[MEMORIA.index(aux)+2]:
            return False
        # Checar LED
    if 'l' in expressao[i:fim]:
        aux = expressao[expressao.index('l', i)+1]
        aux = 'l' + aux
        if not ':' in LED[LED.index(aux)+2]:
            return False

    if not ('+' in expressao[inicio:fim]):
        hasOr = False
    if not ('*' in expressao[inicio:fim]):
        hasAnd = False
    while hasAnd or hasOr:
        auxIndex = 0
        operacao = 0
        if ('+' in expressao[i:fim] and ('*' in expressao[i:fim])):
            if (expressao.index('*', i) < expressao.index('+', i)):
                auxIndex = expressao.index('*', i)
                operacao = 1
                i = expressao.index('*', i)
            if (expressao.index('*', i) > expressao.index('+', i)):
                auxIndex = expressao.index('+', i)
                operacao = 2
                i = expressao.index('+', i)
        elif ('+' in expressao[i:fim]):
            auxIndex = expressao.index('+', i)
            operacao = 2
            i = expressao.index('+', i)
        elif ('*' in expressao[i:fim]):
            auxIndex = expressao.index('*', i)
            operacao = 1
            i = expressao.index('*', i)
        if (operacao != 0):
            # not na frente
            finalOp = auxIndex+3
            inicioOp = auxIndex-2
            if expressao[auxIndex+1] == "!":
                finalOp = finalOp + 1
                if expressao[auxIndex+2] is bool:
                    b = expressao[auxIndex+2]
                elif expressao[auxIndex+2] == 'm':
                    aux = 'm' + expressao[auxIndex+3]
                    b = MEMORIA[MEMORIA.index(aux)+1]
                elif expressao[auxIndex+2] == 'l':
                    aux = 'l' + expressao[auxIndex+3]
                    b = LED[LED.index(aux)+1]
                elif expressao[auxIndex+2] == 'b':
                    b = BTN[auxIndex+2]
            # sem not na frente
            elif expressao[auxIndex+1] is bool:
                b = expressao[auxIndex+1]
            elif expressao[auxIndex+1] == 'm':
                aux = 'm' + expressao[auxIndex+2]
                b = MEMORIA[MEMORIA.index(aux)+1]
            elif expressao[auxIndex+1] == 'l':
                aux = 'l' + expressao[auxIndex+2]
                b = LED[LED.index(aux)+1]
            elif expressao[auxIndex+1] == 'b':
                print("Entro")
                print(auxIndex)
                b = BTN[auxIndex+1]
                print(BTN[auxIndex+1])
            # checar o que vem antes
            if expressao[auxIndex-1] is bool:
                b = expressao[auxIndex-1]
            elif expressao[auxIndex-2] == 'm':
                aux = 'm' + expressao[auxIndex-1]
                b = MEMORIA[MEMORIA.index(aux)+1]
            elif expressao[auxIndex-1] == 'l':
                aux = 'l' + expressao[auxIndex-2]
                b = LED[LED.index(aux)+1]
            elif expressao[auxIndex-2] == 'b':
                b = BTN[auxIndex-2]
            if expressao[auxIndex-3] == '!':
                inicioOp = inicioOp-1
                b = opNot(b)
            if (operacao == 1):
                auxBool = opAnd(a, b)
            if (operacao == 2):
                auxBool = opOr(a, b)
            expressao[inicioOp] = auxBool
            if (fim == finalOp):
                cabo = True
            del expressao[(inicioOp+1):finalOp]

        if not ('+' in expressao[i:fim]):
            hasOr = False
        if not ('*' in expressao[i:fim]):
            hasAnd = False
        i = i + 1
        if (cabo):
            return expressao[inicioOp]
    return expressao[inicioOp]


def valorExpressao(expressao, BTN, LED, MEMORIA):
    if ':' in expressao:
        maiorNivel = int(expressao[expressao.index(':')+1])
        print(maiorNivel)
        inicio = 0
        fim = 0
        aux = 0
        nivel = 0
        i = 0
        hasAbre = True
        hasFecha = True
        while hasAbre or hasFecha:
            if maiorNivel == 1:
                inicio = expressao.index('(')
                fim = expressao.index(')')+1
                auxBool = entreParenteses(
                    expressao, fim, inicio, BTN, LED, MEMORIA)
                print(auxBool)
                expressao[inicio] = auxBool
                del expressao[(inicio+1):fim]
                maiorNivel = -1
            if (nivel == maiorNivel):
                inicio = int(expressao.index('(', i))
                fim = int(expressao.index(')', i)+1)
                auxBool = entreParenteses(
                    expressao, fim, inicio, BTN, LED, MEMORIA)
                print(auxBool)
                expressao[inicio] = auxBool
                del expressao[(inicio+1):fim]
                maiorNivel = maiorNivel-1
                i = 0
            if ('(' in expressao[i:] and ')' in expressao[i:]):
                if (expressao.index('(', i) < expressao.index(')', i)):
                    nivel = nivel + 1
                    i = expressao.index('(', i)
                if (expressao.index('(', i) > expressao.index(')', i)):
                    nivel = nivel - 1
                    i = expressao.index(')', i)
            else:
                hasAbre = False
                if ')' in expressao[i:]:
                    nivel = nivel-1
                    i = expressao.index(')', i)
                else:
                    hasFecha = False
            i = i+1
        return expressao[inicio]
    #
    else:
        return False


# --------------------------------------------------------------------------------------------------------------------------------
# main
# ============================================================================================================================================================================================================================================
LED = ['l1', False, "expressao", 'l2', False, "expressao", 'l3', False, "expressao", 'l4', False, "expressao",
       'l5', False, "expressao", 'l6', False, "expressao", 'l7', False, "expressao", 'l8', False, "expressao",]
BTN = [False, False, False, False, False, False, False, False,]
MEMORIA = ['m1', False, "expressao", 'm2', False, "expressao", 'm3', False, "expressao",
           'm4', False, "expressao", 'm5', False, "expressao", 'm6', False, "expressao"]


# interface info-------------------------------------------------
comando = "(b1+b2)"
run = False

# ---------------------------------------------------------------
# Modo codar
LED[LED.index('l1')+2] = formatacao(comando)

maiorNivel = acharNivel(LED[LED.index('l1')+2])
if (maiorNivel == -1):
    txt = "Entrada {} invalida."
LED[LED.index('l1')+2].append(':')
LED[LED.index('l1')+2].append(str(maiorNivel))

valorExpressao(LED[LED.index('l1')+2], BTN, LED, MEMORIA)
# loop modo run

# while run:
valorExpressao(LED[LED.index('l1')+2], BTN, LED, MEMORIA)


BTN[0] = True
BTN[1] = True


LED[LED.index('l1')+1] = valorExpressao(LED[LED.index('l1')+2],
                                        BTN, LED, MEMORIA)
print(LED[LED.index('l1')+1])
# ============================================================================================================================================================================================================================================
