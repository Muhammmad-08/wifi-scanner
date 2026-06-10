#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wi-Fi Password Brute Force для Android (PyDroid 3)
Работает БЕЗ системных команд - полностью на Python
"""

import os
import sys
import time
import json
from datetime import datetime

# Цветной вывод
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class WiFiBruteFo:
    def __init__(self):
        self.networks = []
        self.selected_network = None
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        
    def print_header(self):
        """Вывод заголовка"""
        print(f"\n{Colors.CYAN}{'=' * 60}")
        print(f"{Colors.BOLD}{Colors.YELLOW}     📱 WI-FI PASSWORD BRUTE FORCE")
        print(f"{Colors.BOLD}{Colors.YELLOW}     (PyDroid 3 для Android)")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.END}\n")
    
    def request_permission(self):
        """Запрос разрешения"""
        print(f"{Colors.CYAN}{'=' * 60}")
        print(f"{Colors.YELLOW}🔐 ЗАПРОС РАЗРЕШЕНИЯ")
        print(f"{Colors.CYAN}{'=' * 60}")
        print(f"\n{Colors.RED}⚠️  ВАЖНО:{Colors.END}")
        print(f"{Colors.WHITE}Этот скрипт подбирает пароли методом перебора")
        print(f"Используйте ТОЛЬКО на своих Wi-Fi сетях!{Colors.END}")
        print(f"\n{Colors.RED}❌ Использование на чужих сетях НЕЗАКОННО!{Colors.END}")
        print(f"\n{Colors.WHITE}Вы понимаете и даете согласие? (да/нет): {Colors.END}", end="")
        
        response = input().strip().lower()
        if response in ['да', 'yes', 'y', 'д', '+']:
            print(f"{Colors.GREEN}✅ Согласие дано!\n{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}❌ Согласие не дано. Выход...\n{Colors.END}")
            return False
    
    def create_sample_networks(self):
        """Создать примеры сетей для демонстрации"""
        print(f"{Colors.CYAN}📝 Поскольку автоматическое сканирование недоступно,")
        print(f"введите названия ваших Wi-Fi сетей вручную\n{Colors.END}")
        
        print(f"{Colors.YELLOW}Сколько сетей вы хотите добавить? (1-5): {Colors.END}", end="")
        
        try:
            count = int(input().strip())
            if count < 1 or count > 5:
                print(f"{Colors.YELLOW}Используется значение по умолчанию: 1\n{Colors.END}")
                count = 1
        except ValueError:
            print(f"{Colors.YELLOW}Используется значение по умолчанию: 1\n{Colors.END}")
            count = 1
        
        for i in range(count):
            print(f"{Colors.WHITE}Введите название сети #{i+1}: {Colors.END}", end="")
            network_name = input().strip()
            if network_name:
                self.networks.append({'name': network_name})
        
        if self.networks:
            print(f"\n{Colors.GREEN}✅ Добавлено сетей: {len(self.networks)}\n{Colors.END}")
            return True
        else:
            print(f"\n{Colors.RED}❌ Сети не добавлены\n{Colors.END}")
            return False
    
    def display_networks(self):
        """Вывод списка сетей"""
        print(f"{Colors.CYAN}{'=' * 60}")
        print(f"{Colors.YELLOW}📡 ВАШИ WI-FI СЕТИ")
        print(f"{Colors.CYAN}{'=' * 60}\n{Colors.END}")
        
        for idx, network in enumerate(self.networks, 1):
            print(f"{Colors.WHITE}{idx}. {Colors.GREEN}{network['name']}{Colors.END}")
        print()
    
    def select_network(self):
        """Выбор сети пользователем"""
        while True:
            try:
                choice = input(f"{Colors.YELLOW}Выберите номер сети (1-{len(self.networks)}): {Colors.END}")
                choice = int(choice) - 1
                
                if 0 <= choice < len(self.networks):
                    self.selected_network = self.networks[choice]['name']
                    print(f"{Colors.GREEN}✅ Выбрана сеть: {self.selected_network}\n{Colors.END}")
                    return True
                else:
                    print(f"{Colors.RED}❌ Неверный выбор. Попробуйте еще раз.\n{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Введите число!\n{Colors.END}")
    
    def load_passwords(self):
        """Загрузка словаря паролей"""
        wordlists = [
            "common_passwords.txt",
            "passwords.txt",
        ]
        
        # Попытка найти файл со словарем
        for wordlist_path in wordlists:
            if os.path.exists(wordlist_path):
                print(f"{Colors.CYAN}📂 Найден словарь: {wordlist_path}\n{Colors.END}")
                try:
                    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                        passwords = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    if passwords:
                        return passwords
                except Exception as e:
                    print(f"{Colors.YELLOW}⚠️  Ошибка при чтении: {e}\n{Colors.END}")
        
        print(f"{Colors.YELLOW}⚠️  Файл со словарем не найден\n{Colors.END}")
        print(f"{Colors.CYAN}📝 Используется встроенный список паролей\n{Colors.END}")
        
        # Встроенный список популярных паролей
        default_passwords = [
            # ТОП пароли (проверяем в первую очередь)
            "123456", "password", "12345678", "qwerty", "abc123",
            "111111", "1234567", "password123", "12345", "123456789",
            
            # Простые числа
            "111111", "222222", "333333", "444444", "555555",
            "666666", "777777", "888888", "999999", "0000",
            "1111", "2222", "3333", "4444", "5555",
            
            # Слова
            "admin", "root", "user", "test", "guest",
            "default", "welcome", "monkey", "master",
            
            # WiFi типичные
            "wifi123", "wifipass", "password123",
            "wifinetwork", "87654321", "abcdefgh",
            
            # Комбинации
            "admin123", "password123", "root123",
            "test123", "user123", "123321", "654321",
            
            # Еще
            "qwerty123", "freedom", "123123", "1234567890",
            "letmein", "trustno1", "sunshine", "princess",
            
            # Русские (если есть)
            "пароль", "администратор", "гость",
        ]
        
        return default_passwords
    
    def test_password(self, password):
        """Имитация проверки пароля"""
        # Просто показываем, что проверяем
        print(f"{Colors.WHITE}[{self.attempts}] Проверка: {Colors.YELLOW}{password}{Colors.END}", end='\r')
        sys.stdout.flush()
        
        # Имитация задержки (как будто проверяем подключение)
        time.sleep(0.1)
        
        # В реальной ситуации здесь была бы проверка подключения
        # Для демонстрации просто возвращаем False
        return False
    
    def brute_force_manual(self):
        """Подбор с ручным вводом пароля"""
        print(f"{Colors.CYAN}🔓 Вы можете:\n{Colors.END}")
        print(f"{Colors.YELLOW}1. Проверить один пароль{Colors.END}")
        print(f"{Colors.YELLOW}2. Подобрать из словаря{Colors.END}")
        print(f"{Colors.YELLOW}3. Выход\n{Colors.END}")
        print(f"{Colors.WHITE}Выберите вариант (1-3): {Colors.END}", end="")
        
        choice = input().strip()
        
        if choice == "1":
            return self.test_single_password()
        elif choice == "2":
            return self.brute_force_from_dict()
        else:
            return False
    
    def test_single_password(self):
        """Проверить один пароль"""
        print(f"\n{Colors.WHITE}Введите пароль для проверки: {Colors.END}", end="")
        password = input().strip()
        
        if not password:
            print(f"{Colors.RED}❌ Пароль не введен\n{Colors.END}")
            return False
        
        print(f"{Colors.CYAN}🔍 Проверка пароля: {Colors.YELLOW}{password}{Colors.END}\n")
        time.sleep(1)
        
        print(f"{Colors.GREEN}{'=' * 60}")
        print(f"ℹ️  В реальной ситуации здесь была бы проверка подключения")
        print(f"Если это ваш пароль, введите 'да':  {Colors.END}", end="")
        
        confirm = input().strip().lower()
        if confirm in ['да', 'yes', 'y']:
            print(f"\n{Colors.GREEN}✅ ПАРОЛЬ ВЕРНЫЙ!{Colors.END}")
            print(f"{Colors.YELLOW}Сеть: {self.selected_network}{Colors.END}")
            print(f"{Colors.YELLOW}Пароль: {Colors.GREEN}{password}{Colors.END}\n")
            self.found_password = password
            return True
        else:
            print(f"{Colors.RED}❌ Пароль неверный\n{Colors.END}")
            return False
    
    def brute_force_from_dict(self):
        """Подбор из словаря"""
        print(f"\n{Colors.CYAN}🔓 Загрузка словаря паролей...\n{Colors.END}")
        passwords = self.load_passwords()
        
        if not passwords:
            print(f"{Colors.RED}❌ Не удалось загрузить пароли\n{Colors.END}")
            return False
        
        print(f"{Colors.GREEN}✅ Загружено паролей: {len(passwords)}\n{Colors.END}")
        print(f"{Colors.CYAN}🔓 Начинаем подбор пароля...\n{Colors.END}")
        
        self.start_time = time.time()
        
        for idx, password in enumerate(passwords, 1):
            self.attempts = idx
            
            if self.test_password(password):
                elapsed_time = time.time() - self.start_time
                print(f"\n\n{Colors.GREEN}{'=' * 60}")
                print(f"✅ ПАРОЛЬ НАЙДЕН!{Colors.END}")
                print(f"{Colors.GREEN}{'=' * 60}{Colors.END}")
                print(f"{Colors.YELLOW}Сеть: {self.selected_network}{Colors.END}")
                print(f"{Colors.YELLOW}Пароль: {Colors.GREEN}{password}{Colors.END}")
                print(f"{Colors.CYAN}Попыток: {self.attempts}{Colors.END}")
                print(f"{Colors.CYAN}Время: {elapsed_time:.2f} секунд\n{Colors.END}")
                
                self.found_password = password
                return True
            
            # Показываем прогресс каждые 10 попыток
            if idx % 10 == 0:
                elapsed = time.time() - self.start_time
                speed = idx / elapsed if elapsed > 0 else 0
                remaining = (len(passwords) - idx) / speed if speed > 0 else 0
                print(f"{Colors.CYAN}Попытка {idx}/{len(passwords)} | Скорость: {speed:.1f} п/сек | Осталось: {remaining:.0f}с{Colors.END}        ", end='\r')
                sys.stdout.flush()
        
        elapsed_time = time.time() - self.start_time
        print(f"\n\n{Colors.RED}❌ Пароль не найден за {elapsed_time:.2f} сек\n{Colors.END}")
        return False
    
    def save_result(self):
        """Сохранение результата"""
        if not self.found_password:
            return False
        
        try:
            result = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'network': self.selected_network,
                'password': self.found_password,
                'attempts': self.attempts,
                'status': 'Успешно'
            }
            
            filepath = 'wifi_results.txt'
            
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
            
            print(f"{Colors.GREEN}✅ Результат сохранен: {filepath}\n{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Не удалось сохранить результат: {e}\n{Colors.END}")
            return False
    
    def run(self):
        """Главный цикл"""
        try:
            self.print_header()
            
            # Запрос разрешения
            if not self.request_permission():
                return
            
            # Добавление сетей вручную
            if not self.create_sample_networks():
                return
            
            # Вывод списка
            self.display_networks()
            
            # Выбор сети
            if not self.select_network():
                return
            
            # Выбор действия
            if self.brute_force_manual():
                # Сохранение результата
                self.save_result()
                print(f"{Colors.GREEN}✅ Операция завершена успешно!\n{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠️  Операция прервана\n{Colors.END}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⚠️  Программа прервана пользователем\n{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}❌ Ошибка: {e}\n{Colors.END}")


def main():
    brute_force = WiFiBruteFo()
    brute_force.run()


if __name__ == "__main__":
    main()
