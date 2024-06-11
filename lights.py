count = 0

# Перебираем все трехзначные числа
for three_digit_number in range(100, 1000):
    # Преобразуем трехзначное число в строку для удобства манипуляций с цифрами
    three_digit_str = str(three_digit_number)

    # Строим пятизначное число с заданными условиями
    five_digit_str = three_digit_str[0] + three_digit_str[1] + three_digit_str[2] + three_digit_str[1] + three_digit_str[0]

    # Переводим полученную строку обратно в целое число
    five_digit_number = int(five_digit_str)

    # Проверяем, делится ли полученное пятизначное число на 9
    if five_digit_number % 9 == 0:
        count += 1

# Выводим результат
print("Количество пятизначных чисел с заданными условиями, делящихся на 9:", count)
