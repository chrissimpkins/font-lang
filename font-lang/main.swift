//
//  main.swift
//  font-lang
//
//  Created by Christopher Simpkins on 11/16/19.
//  Copyright © 2019 Source Foundry Authors. Apache License v2.0
//
import AppKit
import CoreText

// Standard stream functions

func stdout(message: String) {
    let stdout_handle = FileHandle.standardOutput
    stdout_handle.write(Data(message.utf8))
}

func stderr(message: String) {
    let stderr_handle = FileHandle.standardError
    stderr_handle.write(Data(message.utf8))
}

// Font I/O functions

func loadFont(filePath: String, fontSize: CGFloat) -> CTFont {
    let fileURL = URL(fileURLWithPath: filePath) as CFURL
    let fd = CTFontManagerCreateFontDescriptorsFromURL(fileURL) as! [CTFontDescriptor]
    return CTFontCreateWithFontDescriptor(fd[0], fontSize, nil)
}


// Main application logic
let argv = CommandLine.arguments

if argv.count < 2 {
    // Expecting a string but didn't receive it
    stderr(message: "[ERROR] Please enter one or more font paths\n")
    exit(EXIT_FAILURE)
}
else {
    for arg in argv[1...] {
        print("\(arg)")
    }
}




