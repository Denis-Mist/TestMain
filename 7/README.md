# Calculator GUI — QTestLib GUI-тесты

## Qt Creator

1. Открыть `CMakeLists.txt`, kit **Desktop Qt 6.11.2 MinGW 64-bit**.
2. Собрать и запустить **calculator_gui_tests**.

## PowerShell

```powershell
$env:Path = "C:\Qt\Tools\mingw1310_64\bin;C:\Qt\Tools\Ninja;C:\Qt\Tools\CMake_64\bin;" + $env:Path
$src = "C:\Users\Денис\OneDrive\Desktop\7_sem\Тестирование\7"
$build = Join-Path $src "build"
cmake -S $src -B $build -G Ninja -DCMAKE_PREFIX_PATH="C:/Qt/6.11.2/mingw_64" -DCMAKE_BUILD_TYPE=Debug
cmake --build $build
$env:Path = "C:\Qt\6.11.2\mingw_64\bin;" + $env:Path
$env:QT_QPA_PLATFORM = "offscreen"
Set-Location -LiteralPath $build
ctest --output-on-failure
```

Успех: `testAdditionWithGUI`, `testSubtractionWithGUI`, `testInvalidInputShowsError`.
