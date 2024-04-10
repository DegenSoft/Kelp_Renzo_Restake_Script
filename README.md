# Скрипт для заноса в рестейкинг протоколы Kelp и Renzo

## Установка

Всё стандартно

* python 3.10+
* `pip install -r requirements.txt`

## Настройка

Все настройки в  `config.json`

* `network` рабочая сеть, `linea` или `arbitrum`, для Linea нужно отключить модуль kelp
* `modules.kelp` настройки протокола Kelp
* `modules.renzo` настройки протокола Renzo
* `amount` сумма от..до в ETH
* `amount_percent` сумма от..до в процентах от баланса кошелька, если не указано то применяется сумма `amount`
* `enabled` `true` или `false` включает или выключает конкретный модуль
* `random_module` если `true` то берет только один модуль в работу из доступных модулей

