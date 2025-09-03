def show_arrays():
    print("""
📚 Массивы в PAWN:
Массивы хранят несколько значений под одним именем. Примеры:

1. Создание массива:
   new telefon[2] = {"Android", "Apple"};
   
2. Доступ к элементам:
   printf("Первый телефон: %s", telefon[0]);

3. Многомерные массивы (матрицы):
   new matrix[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
   };

4. Строки как массивы символов:
   new message[] = "Привет";
   message[0] = 'X';

🔑 Ключевое:
- Индексация начинается с 0
- Размер массива указывается при объявлении
- Строки заканчиваются нулевым символом (\\0)
""")

def show_variables():
    print("""
📦 Переменные в PAWN:
Переменные хранят данные во время выполнения скрипта.

1. Объявление:
   new playerScore = 100;
   new Float:health = 75.5;

2. Типы данных:
   - Целые числа (new x = 10;)
   - Дробные (Float: new Float:y = 3.14;)
   - Булевы (bool: new bool:isAdmin = true;)

3. Области видимости:
   - Глобальные (вне функций)
   - Локальные (внутри функций)
   - Статические (сохраняют значение между вызовами)

4. Пример:
   new count = 5;
   count += 3; // Теперь 8
   printf("Значение: %d", count);
""")

def show_defines():
    print("""
🎯 #define в PAWN:
Директивы препроцессора для создания констант и макросов.

1. Константы:
   #define MAX_PLAYERS 100
   #define SERVER_NAME "My Server"

2. Макросы:
   #define IsValid(%0) (%0 != INVALID_PLAYER_ID)

3. Условная компиляция:
   #if defined _SAMP
        #include <a_samp>
   #endif

4. Практическое использование:
   if (playerid < MAX_PLAYERS) {
        SendClientMessage(playerid, COLOR_WHITE, "Добро пожаловать!");
   }
""")

def show_systems():
    print("""
🛠️ Создание систем в PAWN:
Системы - комплексные механизмы (регистрация, бизнесы и т.д.)

1. Алгоритм создания системы:
   а) Определить структуру данных
   б) Создать функции управления
   в) Реализовать сохранение/загрузку

2. Пример системы аккаунтов:

   // Глобальные переменные
   enum PlayerData {
        pName[MAX_PLAYER_NAME],
        pPassword[32],
        pScore
   }
   new PlayerInfo[MAX_PLAYERS][PlayerData];

   // Функция регистрации
   public OnPlayerRegister(playerid, password[]) {
        strcpy(PlayerInfo[playerid][pPassword], password, 32);
        PlayerInfo[playerid][pScore] = 0;
   }

   // Сохранение в файл
   public SavePlayerData(playerid) {
        new file[40];
        format(file, sizeof(file), "accounts/%s.ini", PlayerInfo[playerid][pName]);
        // Запись в файл...
   }
""")

def show_commands():
    print("""
⌨️ Создание команд в PAWN:
Команды обрабатывают ввод игрока (/команда)

1. Базовый обработчик:
   public OnPlayerCommandText(playerid, cmdtext[]) {
        if (strcmp("/help", cmdtext, true) == 0) {
            SendClientMessage(playerid, -1, "Справка по командам...");
            return 1;
        }
        return 0;
   }

2. Использование sscanf (рекомендуется):
   CMD:stats(playerid) {
        new targetid;
        if(sscanf(params, "u", targetid)) 
            return SendClientMessage(playerid, -1, "Использование: /stats [игрок]");
        
        new str[128];
        format(str, sizeof(str), "Уровень: %d", PlayerInfo[targetid][pLevel]);
        SendClientMessage(playerid, -1, str);
        return 1;
   }

3. ZCMD + sscanf (оптимально):
   zcmd: /heal [playerid] [amount]
   CMD:heal(playerid, params[]) {
        new targetid, amount;
        if(sscanf(params, "ud", targetid, amount)) 
            return SendClientMessage(playerid, -1, "/heal [id] [кол-во]");
        
        SetPlayerHealth(targetid, amount);
        return 1;
   }
""")

def show_dialog_integration():
    print("""
💬 Интеграция диалогов в команды/системы:
Диалоги используются для сложного взаимодействия с игроком

1. Создание диалога в команде:

   CMD:settings(playerid) {
        ShowPlayerDialog(playerid, DIALOG_SETTINGS, DIALOG_STYLE_LIST, 
            "Настройки", "Чат\nЗвуки\nУправление", "Выбрать", "Назад");
        return 1;
   }

2. Обработка ответа в OnDialogResponse:

   public OnDialogResponse(playerid, dialogid, response, listitem, inputtext[]) {
        if(dialogid == DIALOG_SETTINGS && response) {
            switch(listitem) {
                case 0: ShowChatSettings(playerid);
                case 1: ShowSoundSettings(playerid);
                case 2: ShowControlSettings(playerid);
            }
        }
        return 1;
   }

3. Многошаговая система (регистрация):

   CMD:register(playerid) {
        ShowPlayerDialog(playerid, DIALOG_REG_EMAIL, DIALOG_STYLE_INPUT, 
            "Регистрация", "Введите ваш email:", "Далее", "Отмена");
        return 1;
   }

   // В OnDialogResponse:
   case DIALOG_REG_EMAIL:
        if(!response) return 1;
        if(ValidateEmail(inputtext)) {
            gPlayerTempEmail[playerid] = inputtext; // Сохраняем временные данные
            ShowPlayerDialog(playerid, DIALOG_REG_PASS, DIALOG_STYLE_PASSWORD, 
                "Регистрация", "Придумайте пароль:", "Завершить", "Назад");
        } else {
            ShowError(playerid, "Неверный email!");
        }
        break;
""")

def show_connecting_dialogs():
    print("""
🔌 Подключение диалогов и команд:
Как связать разные компоненты системы

1. Создание диалога:

   // В начале скрипта
   #define DIALOG_LOGIN 1
   #define DIALOG_BANK 2

   // При входе игрока
   public OnPlayerConnect(playerid) {
        ShowPlayerDialog(playerid, DIALOG_LOGIN, DIALOG_STYLE_INPUT, 
            "Авторизация", "Введите пароль:", "Войти", "Выход");
        return 1;
   }

2. Связь команды с диалогом:

   CMD:bank(playerid) {
        if(!IsPlayerNearBank(playerid)) 
            return SendClientMessage(playerid, COLOR_RED, "Вы не в банке!");
        
        ShowPlayerDialog(playerid, DIALOG_BANK, DIALOG_STYLE_LIST, 
            "Банк", "Баланс\nПоложить\nСнять", "Выбрать", "Закрыть");
        return 1;
   }

3. Переход между диалогами (каскадные меню):

   public OnDialogResponse(playerid, dialogid, response, listitem, inputtext[]) {
        if(dialogid == DIALOG_BANK && response) {
            switch(listitem) {
                case 0: ShowBalance(playerid); // Открывает DIALOG_BALANCE
                case 1: ShowDepositDialog(playerid); // DIALOG_DEPOSIT
                case 2: ShowWithdrawDialog(playerid); // DIALOG_WITHDRAW
            }
        }
        return 1;
   }

4. Глобальные переменные для передачи данных:
   new gDialogCache[MAX_PLAYERS][128]; // Буфер для данных между диалогами

   // В команде:
   CMD:report(playerid) {
        gDialogCache[playerid] = 0; // Сброс кэша
        ShowPlayerDialog(playerid, DIALOG_REPORT_TYPE, ...);
   }

   // В обработчике диалога:
   case DIALOG_REPORT_TYPE:
        gDialogCache[playerid] = listitem; // Сохраняем тип репорта
        ShowPlayerDialog(playerid, DIALOG_REPORT_DETAILS, ...);
        break;
""")

def main():
    menu = """
=== PAWN ДЛЯ НАЧИНАЮЩИХ ===


Выберите тему для изучения:
	
1. 📚 Массивы
2. 📦 Переменные
3. 🎯 #define
4. 🛠️ Системы
5. ⌨️ Команды
6. 💬 Диалоги в командах/системах
7. 🔌 Подключение диалогов/команд
0. 🚪 Выход

BY MISTER ODIN
Введите цифру темы > """
    
    while True:
        choice = input(menu).strip()
        
        if choice == "1":
            show_arrays()
        elif choice == "2":
            show_variables()
        elif choice == "3":
            show_defines()
        elif choice == "4":
            show_systems()
        elif choice == "5":
            show_commands()
        elif choice == "6":
            show_dialog_integration()
        elif choice == "7":
            show_connecting_dialogs()
        elif choice == "0":
            print("Удачи в изучении PAWN! 👋")
            break
        else:
            print("❌ Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()