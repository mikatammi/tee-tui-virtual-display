import qbs

DynamicLibrary {
    name: "tuiprotocol"
    Depends { name: "cpp" }
    cpp.includePaths: ["include"]

    destinationDirectory: '.'

    Export {
        Depends { name: "cpp" }
        cpp.includePaths: "include"
    }

    files: [
        "include/tui_protocol.h",
        "src/tui_protocol.c"
    ]
}
