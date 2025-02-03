# futures-predictions-nlp

## Настройка окружения

### Начало работы

Для начала работы с проектом клонируйте репозиторий:

```bash
git clone https://github.com/kosarenok/futures-predictions-nlp.git
```

Создайте виртуальное окружение

```bash
python -m venv .venv
```

Активируйте виртуальное окружение:

```bash
# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Переменные окружения

Для работы над проектом необходим файл `.env`.
Создайте его в корне проекта и заполните переменные окружения собственными кредами, за основу возьмите файл
`.env.example`

Переменная окружения PYTHONPATH должна быть всегда в значении пути до проекта.

```bash
# Linux
export PYTHONPATH=$(pwd)

# Windows
set PYTHONPATH=%cd%
```