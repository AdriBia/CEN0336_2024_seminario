#!/usr/bin/env python3

#Definindo a exceção personalizada NotATCG
class NotATCG(Exception):
    pass

#Definindo a exceção personalizada Notdigit
class Notdigit(Exception):
    pass


try:
    file01 = input("Digite o nome do primeiro arquivo (extensões válidas: .fasta, .fa, .nt): ").strip()

    file02 = input("Digite o nome do segundo arquivo (extensões válidas: .fasta, .fa, .nt): ").strip()

    # Validação das sequências
    # Verificar se o arquivo tem a extensão correta
    if not (file01.endswith('.fasta') or file01.endswith('.fa') or file01.endswith('.nt') or file02.endswith('.fasta') or file02.endswith('.fa') or file02.endswith('.nt')):
        raise ValueError("Os arquivos devem ter uma das seguintes extensões '.fasta', '.fa' ou '.nt'.")

    # Comparação das sequências para identificação de SNPs
    print("Comparando sequências...")

    # Lendo o primeiro arquivo e salvando o ID e a sequência
    name01 = ""
    seq01 = ""
    with open(file01, "r") as FASTA01:
        for line in FASTA01:
            line = line.rstrip()
            if line.startswith('>'):
                name01 = line
            else:
                # Transformando toda a sequência para letra maiúscula e acumulando como uma string
                seq01 += line.upper()

    # Lendo o segundo arquivo e salvando o ID e a sequência
    name02 = ""
    seq02 = ""
    with open(file02, "r") as FASTA02:
        for line in FASTA02:
            line = line.rstrip()
            if line.startswith('>'):
                name02 = line
            else:
                # Transformando toda a sequência para letra maiúscula e acumulando como uma string
                seq02 += line.upper()

    # Verificando se não há outros caracteres dentro das sequências
    if not set(seq01).issubset(set("ATCGN")) or not set(seq02).issubset(set("ATCGN")):
        raise NotATCG("Erro: Outros caracteres, além desse conjunto A, T, C, G or (N), foram encontrados nesta sequência. Verifique sua sequência!")

    # Alinhando as sequências - recebendo a posição do primeiro nucleotídeo
    posi01 = input("Informe a posição inicial do primeiro nucleotídeo da sequência 01: ")

    posi02 = input("Informe a posição inicial do primeiro nucleotídeo da sequência 02: ")

    # Verificando se as posição de input são apenas dígitos numéricos
    if not posi01.isdigit() or not posi02.isdigit():
      raise Notdigit01("Erro: A posição do primeiro nucleptídeo da sequência deve ser apenas dígitos númericos")

    # Transformando a variável em número inteiro
    posi01 = int(posi01)
    posi02 = int(posi02)

    # Ajustando a posição incia da sequência
    add01 = "x" * (posi01 - 1)
    seq01 = add01 + seq01
    add02 = "x" * (posi02 - 1)
    seq02 = add02 + seq02

    # Ajustando o tamanho final das sequências - deixando elas com o mesmo tamanho
    end01 = len(seq01)
    end02 = len(seq02)
    if end01 > end02:
      add_end02 = "x" * (end01 - end02)
      seq02 = seq02 + add_end02
    else:
      add_end01 = "x" * (end02 - end01)
      seq01 = seq01 + add_end01

    # Buscando pelos SNPs
    snps = []
    # Define o intervalo mínimo de correspondência entre as sequências ao de redor do SNP
    inter = input("Informe o número mínimo de pares de bases que devem corresponder ao redor do SNP: ")

    # Verificando se o intervalo de correspondência é um dígito numérico
    if not inter.isdigit():
      raise Notdigit02("Erro: O intervalo de correspondência das sequências deve ser apenas dígitos númericos")

    # Sinalização de início do processo ao usuário
    print("Processando...")

    inter = int(inter)
    # Alinhando as sequências
    for i in range(min(len(seq01), len(seq02))):
        if (seq01[i] != "x" and seq02[i] != "x") and (seq01[i] != "N" and seq02[i] != "N"):
          if seq01[i] != seq02[i]:
            # Verificando se os índices estão dentro do intervalo válido antes de acessá-los
            if (i - inter - 1 >= 0 and i + 1 + inter < len(seq01) and
              seq01[i - inter:i] == seq02[i - inter:i] and
              seq01[i + 1:i + 1 + inter] == seq02[i + 1:i + 1 + inter] and
              (set(seq01[i - inter:i + 1 + inter]).issubset(set("ATCG")) and set(seq02[i - inter:i + 1 + inter]).issubset(set("ATCG")))):

              snps.append((i, seq01[i], seq02[i]))

    # Armazenamento e exibição dos SNPs
    if snps:
        print("SNPs identificados:")
        for pos, base1, base2 in snps:
            print(f"SNP identificado na posição {pos}: {base1} -> {base2}")
        # Exibição da contagem de SNPs
        print(f"Total de {len(snps)} SNPs identificados.")
    else:
        print("Nenhum SNP identificado.")
    # Exibição da contagem de SNPs
    #print(f"Total de {len(snps)} SNPs identificados.")

except ValueError:
    print("O arquivo deve ter uma das seguintes extensões '.fasta', '.fa' ou '.nt'.")
# Se uma entrada não é fornecida
except IndexError:
    print("Error: Please provide a file name")
# Se o arquivo não pode ser aberto
except IOError:
    print("Error: Can't find file:", file01)
# Presença de outros caracteres, além de ATCG
except NotATCG:
    print("Erro: Outros caracteres, além desse conjunto A, T, C, G or (N), foram encontrados nesta sequência. Verifique sua sequência!")
# Posição do primeiro nucleotídio errado
except Notdigit01:
    print("Erro: A posição do primeiro nucleptídeo da sequência deve ser apenas dígitos númericos")
# Intervalo de correspondência errado
except Notdigit02:
    print("Erro: O intervalo de correspondência das sequências deve ser apenas dígitos númericos")
else:
    print("O programa foi executado com sucesso! Todas as etapas foram concluídas corretamente.")
