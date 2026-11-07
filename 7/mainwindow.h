#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

class QLineEdit;
class QPushButton;
class QLabel;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private slots:
    void onAddClicked();
    void onSubtractClicked();

private:
    void setupUi();
    int readOperand(QLineEdit *edit, bool *ok) const;

    QLineEdit *m_input1 = nullptr;
    QLineEdit *m_input2 = nullptr;
    QPushButton *m_addButton = nullptr;
    QPushButton *m_subtractButton = nullptr;
    QLabel *m_resultLabel = nullptr;
    QLabel *m_errorLabel = nullptr;
};

#endif
