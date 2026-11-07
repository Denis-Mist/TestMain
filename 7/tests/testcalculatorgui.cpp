#include "testcalculatorgui.h"

#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QTest>

#include "mainwindow.h"

void TestCalculatorGUI::testAdditionWithGUI()
{
    MainWindow window;
    window.show();
    QVERIFY(QTest::qWaitForWindowExposed(&window));

    auto *input1 = window.findChild<QLineEdit *>(QStringLiteral("input1"));
    auto *input2 = window.findChild<QLineEdit *>(QStringLiteral("input2"));
    auto *addButton = window.findChild<QPushButton *>(QStringLiteral("addButton"));
    auto *resultLabel = window.findChild<QLabel *>(QStringLiteral("resultLabel"));

    QVERIFY(input1);
    QVERIFY(input2);
    QVERIFY(addButton);
    QVERIFY(resultLabel);

    QTest::keyClicks(input1, QStringLiteral("15"));
    QTest::keyClicks(input2, QStringLiteral("7"));
    QTest::mouseClick(addButton, Qt::LeftButton);

    QCOMPARE(resultLabel->text(), QStringLiteral("22"));
    QVERIFY(input1->text().isEmpty());
    QVERIFY(input2->text().isEmpty());
}

void TestCalculatorGUI::testSubtractionWithGUI()
{
    MainWindow window;
    window.show();
    QVERIFY(QTest::qWaitForWindowExposed(&window));

    auto *input1 = window.findChild<QLineEdit *>(QStringLiteral("input1"));
    auto *input2 = window.findChild<QLineEdit *>(QStringLiteral("input2"));
    auto *subtractButton = window.findChild<QPushButton *>(QStringLiteral("subtractButton"));
    auto *resultLabel = window.findChild<QLabel *>(QStringLiteral("resultLabel"));

    QTest::keyClicks(input1, QStringLiteral("30"));
    QTest::keyClicks(input2, QStringLiteral("12"));
    QTest::mouseClick(subtractButton, Qt::LeftButton);

    QCOMPARE(resultLabel->text(), QStringLiteral("18"));
}

void TestCalculatorGUI::testInvalidInputShowsError()
{
    MainWindow window;
    window.show();
    QVERIFY(QTest::qWaitForWindowExposed(&window));

    auto *input1 = window.findChild<QLineEdit *>(QStringLiteral("input1"));
    auto *input2 = window.findChild<QLineEdit *>(QStringLiteral("input2"));
    auto *addButton = window.findChild<QPushButton *>(QStringLiteral("addButton"));
    auto *errorLabel = window.findChild<QLabel *>(QStringLiteral("errorLabel"));

    QTest::keyClicks(input1, QStringLiteral("abc"));
    QTest::keyClicks(input2, QStringLiteral("5"));
    QTest::mouseClick(addButton, Qt::LeftButton);

    QCOMPARE(errorLabel->text(), QStringLiteral("Invalid input"));
}
