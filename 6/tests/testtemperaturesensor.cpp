#include "testtemperaturesensor.h"

#include <QSignalSpy>
#include <QTest>

#include "temperaturesensor.h"

void TestTemperatureSensor::testSignalEmittedOnChange()
{
    TemperatureSensor sensor;
    QSignalSpy spy(&sensor, &TemperatureSensor::temperatureChanged);

    sensor.setTemperature(25);

    QCOMPARE(spy.count(), 1);
}

void TestTemperatureSensor::testSignalCarriesCorrectValue()
{
    TemperatureSensor sensor;
    QSignalSpy spy(&sensor, &TemperatureSensor::temperatureChanged);

    sensor.setTemperature(25);

    QCOMPARE(spy.count(), 1);
    const QList<QVariant> arguments = spy.takeFirst();
    QCOMPARE(arguments.at(0).toInt(), 25);
    QCOMPARE(sensor.temperature(), 25);
}

void TestTemperatureSensor::testSignalNotEmittedOnSameValue()
{
    TemperatureSensor sensor;
    sensor.setTemperature(25);

    QSignalSpy spy(&sensor, &TemperatureSensor::temperatureChanged);
    sensor.setTemperature(25);

    QCOMPARE(spy.count(), 0);
    QCOMPARE(sensor.temperature(), 25);
}
