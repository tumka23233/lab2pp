import re
import unittest

class CardValidator:
    def __init__(self):
        # Регулярное выражение ищет последовательности от 13 до 19 цифр,
        # которые могут быть разделены пробелами или дефисами
        self.pattern = re.compile(r"\b(?:\d[ -]*?){13,19}\b")

    def _luhn_check(self, card_number: str) -> bool:
        """Внутренний метод проверки номера карты по алгоритму Луна."""
        digits = [int(d) for d in card_number if d.isdigit()]

        # Если после очистки длина не соответствует стандарту, карта невалидна
        if not (13 <= len(digits) <= 19):
            return False

        # Алгоритм Луна: удваиваем каждую вторую цифру, начиная с конца
        checksum = 0
        reverse_digits = digits[::-1]

        for i, digit in enumerate(reverse_digits):
            if i % 2 == 1:
                double_digit = digit * 2
                # Если результат удвоения больше 9, вычитаем 9 (что равносильно сумме цифр числа)
                checksum += double_digit if double_digit < 9 else double_digit - 9
            else:
                checksum += digit

        # Номер корректен, если итоговая сумма делится на 10 без остатка
        return checksum % 10 == 0

    def validate_text(self, text: str) -> list:
        """Поиск всех синтаксически корректных номеров карт в тексте."""
        potential_cards = self.pattern.findall(text)
        valid_cards = []

        for card in potential_cards:
            # Очищаем найденный кандидат от лишних пробелов/дефисов для проверки Луна
            cleaned_card = "".join(card.split()).replace("-", "")
            # Если кандидат проходит алгоритм Луна, добавляем исходное форматирование в результат
            if self._luhn_check(cleaned_card):
                valid_cards.append(card.strip())

        return valid_cards

    def validate_file(self, filepath: str) -> list:
        """Чтение файла и поиск номеров карт в его содержимом."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return self.validate_text(f.read())
        except FileNotFoundError:
            return []

class TestCardValidator(unittest.TestCase):
    def setUp(self):
        self.validator = CardValidator()

    def test_valid_cards(self):
        # Тест с реальными валидными номерами карт (тестовые карты Visa и Mastercard)
        text = "Оплата по картам 49927398716 и 5412-7512-3412-3456 прошла успешно."
        result = self.validator.validate_text(text)
        self.assertEqual(result, ["49927398716", "5412-7512-3412-3456"])

    def test_invalid_cards(self):
        # Тест с картами, где цифры подобраны случайно (не пройдут алгоритм Луна)
        text = "Неверные номера: 1234-5678-1234-5678, а также слишком короткий 123"
        result = self.validator.validate_text(text)
        self.assertEqual(result, [])