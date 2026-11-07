#include "mainwindow.h"

#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QWidget>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setupUi();
}

void MainWindow::setupUi()
{
    auto *central = new QWidget(this);
    auto *layout = new QGridLayout(central);

    m_input1 = new QLineEdit(central);
    m_input1->setObjectName(QStringLiteral("input1"));

    m_input2 = new QLineEdit(central);
    m_input2->setObjectName(QStringLiteral("input2"));

    m_addButton = new QPushButton(QStringLiteral("+"), central);
    m_addButton->setObjectName(QStringLiteral("addButton"));

    m_subtractButton = new QPushButton(QStringLiteral("−"), central);
    m_subtractButton->setObjectName(QStringLiteral("subtractButton"));

    m_resultLabel = new QLabel(QStringLiteral("—"), central);
    m_resultLabel->setObjectName(QStringLiteral("resultLabel"));

    m_errorLabel = new QLabel(central);
    m_errorLabel->setObjectName(QStringLiteral("errorLabel"));
    m_errorLabel->setStyleSheet(QStringLiteral("color: red;"));

    layout->addWidget(new QLabel(QStringLiteral("A:")), 0, 0);
    layout->addWidget(m_input1, 0, 1);
    layout->addWidget(new QLabel(QStringLiteral("B:")), 1, 0);
    layout->addWidget(m_input2, 1, 1);
    layout->addWidget(m_addButton, 2, 0);
    layout->addWidget(m_subtractButton, 2, 1);
    layout->addWidget(new QLabel(QStringLiteral("Result:")), 3, 0);
    layout->addWidget(m_resultLabel, 3, 1);
    layout->addWidget(m_errorLabel, 4, 0, 1, 2);

    setCentralWidget(central);
    setWindowTitle(QStringLiteral("Calculator GUI"));

    connect(m_addButton, &QPushButton::clicked, this, &MainWindow::onAddClicked);
    connect(m_subtractButton, &QPushButton::clicked, this, &MainWindow::onSubtractClicked);
}

int MainWindow::readOperand(QLineEdit *edit, bool *ok) const
{
    return edit->text().trimmed().toInt(ok);
}

void MainWindow::onAddClicked()
{
    bool ok1 = false;
    bool ok2 = false;
    const int a = readOperand(m_input1, &ok1);
    const int b = readOperand(m_input2, &ok2);

    if (!ok1 || !ok2) {
        m_errorLabel->setText(QStringLiteral("Invalid input"));
        m_resultLabel->setText(QStringLiteral("—"));
        return;
    }

    m_errorLabel->clear();
    m_resultLabel->setText(QString::number(a + b));
    m_input1->clear();
    m_input2->clear();
}

void MainWindow::onSubtractClicked()
{
    bool ok1 = false;
    bool ok2 = false;
    const int a = readOperand(m_input1, &ok1);
    const int b = readOperand(m_input2, &ok2);

    if (!ok1 || !ok2) {
        m_errorLabel->setText(QStringLiteral("Invalid input"));
        m_resultLabel->setText(QStringLiteral("—"));
        return;
    }

    m_errorLabel->clear();
    m_resultLabel->setText(QString::number(a - b));
    m_input1->clear();
    m_input2->clear();
}
