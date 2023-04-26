
import os
import functions


def logger(path):
    ...

    def __logger(old_function):
        def new_function(*args, **kwargs):
            old_function_name = old_function.__name__
            print(f'Вызов функции {old_function_name} c аргументами {args}{kwargs}')

            datetime_now = functions.get_datetime_now()
            date_today = datetime_now[0]
            time_now = datetime_now[1]
            print(f'Дата вызова функции {date_today}, время вызова: {time_now}')

            result = old_function(*args, **kwargs)
            print(f'Результат : {result}')

            log_data = f'{old_function.__name__}, {args},{kwargs}, {date_today}, {time_now}, {result} \n'
            functions.write_log(path, log_data)

            return result

        return new_function

    return __logger
@logger('flat_generator.log')
def flat_generator(list_of_lists):
    for el in list_of_lists:
        for i in el:
            yield i

flat_generator([
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ])


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()

