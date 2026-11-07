# TemperatureSensor — QSignalSpy (QTestLib)

## Qt Creator

1. **File → Open File or Project** → `CMakeLists.txt` в этой папке.
2. Kit: **Desktop Qt 6.11.2 MinGW 64-bit**.
3. Запустите target **temperature_sensor_tests**.

## PowerShell

```powershell
$env:Path = "C:\Qt\Tools\mingw1310_64\bin;C:\Qt\Tools\Ninja;C:\Qt\Tools\CMake_64\bin;" + $env:Path
$src = "C:\Users\Денис\OneDrive\Desktop\7_sem\Тестирование\6"
$build = Join-Path $src "build"
cmake -S $src -B $build -G Ninja -DCMAKE_PREFIX_PATH="C:/Qt/6.11.2/mingw_64" -DCMAKE_BUILD_TYPE=Debug
cmake --build $build
$env:Path = "C:\Qt\6.11.2\mingw_64\bin;" + $env:Path
Set-Location -LiteralPath $build
ctest --output-on-failure
```

Успех: три теста — `testSignalEmittedOnChange`, `testSignalCarriesCorrectValue`, `testSignalNotEmittedOnSameValue`.
