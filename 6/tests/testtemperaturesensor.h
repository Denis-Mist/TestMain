#ifndef TESTTEMPERATURESENSOR_H
#define TESTTEMPERATURESENSOR_H

#include <QObject>

class TestTemperatureSensor : public QObject
{
    Q_OBJECT

private slots:
    void testSignalEmittedOnChange();
    void testSignalCarriesCorrectValue();
    void testSignalNotEmittedOnSameValue();
};

#endif
