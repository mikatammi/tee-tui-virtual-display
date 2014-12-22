import qbs

CppApplication {
    name: 'virtualdisplay-qt'

    Depends { name: 'tuiprotocol'}

    Depends {
        name: "Qt"
        submodules: ["gui", "widgets"]
    }

    files: [
        'main.cpp',
        'mainwindow.cpp',
        'mainwindow.h',
        'mainwindow.ui',
        'settingsdialog.cpp',
        'settingsdialog.h',
        'settingsdialog.ui'
    ]
}
