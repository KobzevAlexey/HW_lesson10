def calc_main(string):
    from datetime import datetime
    def parce_input(chars):
        try:  # Функция для обработки входных данных, избавляется от пробелов и выдает массив из операций, скобок и чисел
            chars = chars.replace(' ', '')  # Теперь можно не соблюдать пробелы при вводе данных
        except:
            pass
        result = []
        temp = ''
        for i in range(len(chars)):
            if chars[i].isdigit() or (chars[i] == '-' and not chars[i - 1].isdigit()):
                temp += chars[i]
            else:
                if temp.isdigit() or (temp.startswith('-') and len(temp) > 1):
                    result.append(int(temp))
                result.append(chars[i])
                temp = ''
        if len(temp) > 0:
            result.append(int(temp))
        return result

    def calculate(args):

        def find_closing(args):  # Функция для поиска закрывающей скобки в строке
            count = 0
            for i in range(args.index('('), len(args)):  # начинаем поиск с первой открывающей скобки
                if args[i] == '(':  # попалась открывающая, делаем +1
                    count += 1
                if args[i] == ')':  # попалась закрывающая, делаем -1
                    count -= 1
                if count == 0:  # вышли в ноль - закрывающая скобка найдена, возвращаем индекс
                    return i

        while '(' in args and ')' in args:  # Избавляемся от скобок при помощи рекурсии: на выражение в скобках вызываем эту же функцию
            args[args.index('('): find_closing(args) + 1] = [calculate(args[args.index('(') + 1: find_closing(args)])]

        while '*' in args or '/' in args:  # Далее все по семинару
            try:
                ind_mul = args.index('*')
            except:
                ind_mul = 10000
            try:
                ind_dev = args.index('/')
            except:
                ind_dev = 10000
            if ind_mul < ind_dev:
                args[ind_mul - 1] = args[ind_mul - 1] * args[ind_mul + 1]
                args.pop(ind_mul + 1)
                args.pop(ind_mul)

            if ind_mul > ind_dev:
                args[ind_dev - 1] = args[ind_dev - 1] / args[ind_dev + 1]
                args.pop(ind_dev + 1)
                args.pop(ind_dev)

        while '+' in args or '-' in args:
            try:
                ind_sum = args.index('+')
            except:
                ind_sum = 10000
            try:
                ind_deg = args.index('-')
            except:
                ind_deg = 10000
            if ind_sum < ind_deg:
                args[ind_sum - 1] = args[ind_sum - 1] + args[ind_sum + 1]
                args.pop(ind_sum + 1)
                args.pop(ind_sum)

            if ind_sum > ind_deg:
                args[ind_deg - 1] = args[ind_deg - 1] - args[ind_deg + 1]
                args.pop(ind_deg + 1)
                args.pop(ind_deg)

        return args[0]

    result = calculate(parce_input(string))
    with open('log_calc.txt', 'a') as output_file:
        data = datetime.now().strftime('%Y.%m.%d %H:%M:%S  ')
        output_file.writelines(f'{data} {string} = {result}\n')
    return f'результат равен {result}'
