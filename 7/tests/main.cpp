#include "testcalculatorgui.h"

#include <QApplication>
#include <QTest>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    TestCalculatorGUI test;
    return QTest::qExec(&test, argc, argv);
}
