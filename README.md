# TestMain

Практики 6–16 по тестированию. Прогон на GitHub Actions (удалённый runner), не на локальном компьютере.

| Папка | Что запускает workflow |
|-------|------------------------|
| `6`, `7` | Qt 6 / QTest, `ctest` |
| `8`, `9` | Apache JMeter, httpbin.org |
| `12`–`15` | проекты Selenium IDE (`.side`) через `runner/run_side.py` |
| `16` | pytest + Selenium |
| `10`, `11` | скриншоты и замеры вёрстки detmir.ru, Lighthouse |

Результаты пишутся в `screenshots/` и `ci-summary.md` отдельным коммитом.
