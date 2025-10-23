def economizando():
    while True:
        inicio = input("Olá, bem vindo ao economic! Vamos começa? (s/n): ").upper()
        if inicio == 'S':
            print("Ótimo! Vamos lá.")
            Salário = float(input("Digite o valor do seu salário mensal: R$ "))
            Gastos = float(input("Digite o valor total dos seus gastos mensais: R$ "))
            porc = (Gastos / Salário) * 100
            print(f"Você está gastando {porc:.2f}% do seu salário.")
            Anual = (Salário - Gastos)
            while True:
                opção1 = int(input("Deseja calcular uma meta de economia?(digite 1), ou média anual de economia?(digite 2) "))
                if opção1 == 1:
                    prazo = int(input("Em quantos meses você deseja atingir sua meta de economia? "))
                    print(f"Com base nos valores informados, ao final do prazo você terá acumulado R${Anual*prazo}")
                    break
                elif opção1 == 2:
                    print(f"Sua média anual de economia é de R${Anual*12}")
                    break
                else:   
                    print("Opção inválida. Tente novamente.")
            break
        
        elif inicio == 'N':
            print("Tudo bem, até a próxima!")
            break
        else:
            print("Opção inválida. Por favor, responda com 's' ou 'n'.")
economizando()


             