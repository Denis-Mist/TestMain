#include "temperaturesensor.h"

TemperatureSensor::TemperatureSensor(QObject *parent)
    : QObject(parent)
{
}

int TemperatureSensor::temperature() const
{
    return m_temperature;
}

void TemperatureSensor::setTemperature(int value)
{
    if (m_temperature == value) {
        return;
    }
    m_temperature = value;
    emit temperatureChanged(m_temperature);
}
