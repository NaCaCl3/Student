#include <iostream> // ввод/вывод
#include <string> // работа со строками
#include <sstream> // преобразование строк в числа
#include <iomanip> // форматирование вывода

int a = 0; 
int b = 0; 
int result = 0; 

// функция для ввода шестнадцатиричного числа, принимает строку подсказку, возвращает число в десятичном виде 

int inputHex(std::string prompt) {
	std::string input;
	int number;
	std::cout << prompt;
	getline(std::cin, input);
	std::stringstream ss; // поток для образования строки в число
	ss << std::hex << input; // запись строки в поток, hex - означает, что число в шестнадцатиричной системе
	ss >> number;
	return number;
}

// функция сложения на ассемблере, принимает 2 числа и возвращает их сумму

int addAsm(int x, int y) {
	int result_asm = 0;
	__asm {
		mov eax, x// загружаем первое число
		mov ebx, y // загружаем второе число
		add eax, ebx // складываем в eax
		mov result_asm, eax // сохраняем результат из eax в переменную
							// описываем, какие регистры используем
	}
	return result_asm;
}

int main()
{
	setlocale(LC_ALL, "RU");
	std::cout << "=======================" << std::endl;
	std::cout << "Введите числа в HEX (Например: 1F, A3, 100)" << std::endl;
	a = inputHex("Введите первое число в HEX ");
	b = inputHex("Введите второе число в HEX ");
	result = addAsm(a, b);

	std::cout << "Результат: " << result;
	return 0;
}