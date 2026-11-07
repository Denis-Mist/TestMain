#ifndef TESTCALCULATORGUI_H
#define TESTCALCULATORGUI_H

#include <QObject>

class TestCalculatorGUI : public QObject
{
    Q_OBJECT

private slots:
    void testAdditionWithGUI();
    void testSubtractionWithGUI();
    void testInvalidInputShowsError();
};

#endif
