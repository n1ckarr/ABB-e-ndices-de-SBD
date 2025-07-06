class Registro:
    def __init__(self, cpf, nome, data_nascimento):
        self.cpf = cpf  
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.deletado = False  
    
    def __lt__(self, outro):
        return self.cpf < outro.cpf
    
    def __str__(self):
        return f"CPF: {self.cpf}, Nome: {self.nome}, Nascimento: {self.data_nascimento}"


class NoABB:
    def __init__(self, registro, posicao):
        self.registro = registro
        self.posicao = posicao  
        self.esquerda = None
        self.direita = None


class ABB:
    def __init__(self, dados=None):
        self.raiz = None
        if dados is not None:
            for registro in dados:
                self.inserir(registro)
    
    def inserir(self, registro, posicao):
        novo_no = NoABB(registro, posicao)
        if self.raiz is None:
            self.raiz = novo_no
        else:
            self._inserir_rec(self.raiz, novo_no)
    
    def _inserir_rec(self, atual, novo_no):
        if novo_no.registro < atual.registro:
            if atual.esquerda is None:
                atual.esquerda = novo_no
            else:
                self._inserir_rec(atual.esquerda, novo_no)
        else:
            if atual.direita is None:
                atual.direita = novo_no
            else:
                self._inserir_rec(atual.direita, novo_no)
    
    def buscar(self, cpf):
        return self._buscar_rec(self.raiz, cpf)
    
    def _buscar_rec(self, no, cpf):
        if no is None:
            return None
        if cpf == no.registro.cpf:
            return no
        elif cpf < no.registro.cpf:
            return self._buscar_rec(no.esquerda, cpf)
        else:
            return self._buscar_rec(no.direita, cpf)
    
    def remover(self, cpf):
        self.raiz = self._remover_rec(self.raiz, cpf)
    
    def _remover_rec(self, no, cpf):
        if no is None:
            return None
        
        if cpf < no.registro.cpf:
            no.esquerda = self._remover_rec(no.esquerda, cpf)
        elif cpf > no.registro.cpf:
            no.direita = self._remover_rec(no.direita, cpf)
        else:
            
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            
            
            temp = self._min_valor_no(no.direita)
            no.registro = temp.registro
            no.posicao = temp.posicao
            no.direita = self._remover_rec(no.direita, temp.registro.cpf)
        
        return no
    
    def _min_valor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
    
    def pre_ordem(self):
        self._pre_ordem_rec(self.raiz)
        print()
    
    def _pre_ordem_rec(self, no):
        if no is not None:
            print(no.registro.cpf, end=" ")
            self._pre_ordem_rec(no.esquerda)
            self._pre_ordem_rec(no.direita)
    
    def pos_ordem(self):
        self._pos_ordem_rec(self.raiz)
        print()
    
    def _pos_ordem_rec(self, no):
        if no is not None:
            self._pos_ordem_rec(no.esquerda)
            self._pos_ordem_rec(no.direita)
            print(no.registro.cpf, end=" ")
    
    def em_ordem(self):
        self._em_ordem_rec(self.raiz)
        print()
    
    def _em_ordem_rec(self, no):
        if no is not None:
            self._em_ordem_rec(no.esquerda)
            print(no.registro.cpf, end=" ")
            self._em_ordem_rec(no.direita)
    
    def em_largura(self):
        if self.raiz is None:
            return
        
        fila = [self.raiz]
        while fila:
            no = fila.pop(0)
            print(no.registro.cpf, end=" ")
            
            if no.esquerda is not None:
                fila.append(no.esquerda)
            if no.direita is not None:
                fila.append(no.direita)
        print()


class SistemaGerenciadorBD:
    def __init__(self):
        self.edl = []  
        self.indice = ABB() 
    
    def inserir_registro(self, registro):
        posicao = len(self.edl)
        self.edl.append(registro)
        self.indice.inserir(registro, posicao)
    
    def buscar_registro(self, cpf):
        no = self.indice.buscar(cpf)
        if no is None:
            print("Registro não encontrado.")
            return None
        
        registro = self.edl[no.posicao]
        if registro.deletado:
            print("Registro foi deletado.")
            return None
        
        return registro
    
    def remover_registro(self, cpf):
        no = self.indice.buscar(cpf)
        if no is None:
            print("Registro não encontrado.")
            return False
        
        # Marca como deletado na EDL
        self.edl[no.posicao].deletado = True
        # Remove do índice
        self.indice.remover(cpf)
        return True
    
    def gerar_edl_ordenada(self):
        edl_ordenada = []
        self._gerar_edl_ordenada_rec(self.indice.raiz, edl_ordenada)
        return edl_ordenada
    
    def _gerar_edl_ordenada_rec(self, no, lista):
        if no is not None:
            self._gerar_edl_ordenada_rec(no.esquerda, lista)
            if not self.edl[no.posicao].deletado:
                lista.append(self.edl[no.posicao])
            self._gerar_edl_ordenada_rec(no.direita, lista)