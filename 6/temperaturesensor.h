#ifndef TEMPERATURESENSOR_H
#define TEMPERATURESENSOR_H

#include <QObject>

class TemperatureSensor : public QObject
{
    Q_OBJECT

public:
    explicit TemperatureSensor(QObject *parent = nullptr);

    int temperature() const;
    void setTemperature(int value);

signals:
    void temperatureChanged(int newValue);

private:
    int m_temperature = 0;
};

#endif
