# Правила

Именование коммитов: https://www.conventionalcommits.org/en/v1.0.0/

## Ветки

`git checkout -b <название ветки>`

Название ветки - тип ветки и краткое описание

Примеры:
- `feat/database`
- `fix/model_weights`

## Локальные и мердж коммиты

`git commit -m "<тип коммита>: <краткое оиписание>"`

Типы коммита: feat, fix, feat(ci), fix(refactor)

Примеры

Локальный коммит

`git commit -m "feat: Add new script test.py"`

Для мердж коммита выбираем общее название, описывающее ветку

`feat: New script test.py`

## Линтеры

`pre-commit run --all-files`

либо

`make pre_commit`
