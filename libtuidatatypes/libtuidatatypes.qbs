import qbs

DynamicLibrary {
    name: "tuidatatypes"
    Depends { name: "cpp" }
    cpp.includePaths: ["include"]

    destinationDirectory: '.'

    Export {
        Depends { name: "cpp" }
        cpp.includePaths: "include"
    }

    files: [
        "include/tui_datatypes.h"
    ]
}
