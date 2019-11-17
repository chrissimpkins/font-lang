//
//  main.swift
//  font-lang
//
//  Created by Christopher Simpkins on 11/16/19.
//  Copyright © 2019 Source Foundry Authors. Apache License v2.0
//
import AppKit
import CoreText

// Application data

let VERSION = "0.1.0"
let EXECUTABLE = "font-lang"

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

// Utilities

func fileExists(filePath: String) -> Bool {
    let manager = FileManager.default
    return manager.fileExists(atPath: filePath)
}


// Main application logic
let argv = CommandLine.arguments

// Validation : missing arguments
if argv.count < 2 {
    stderr(message: "[ERROR] Please enter one or more font paths\n")
    exit(EXIT_FAILURE)
}

// TODO: add help, usage, version support

// Validation: file paths exist
for arg in argv[1...] {
    if !fileExists(filePath: arg) {
        stderr(message: "[ERROR] The file '\(arg)' does not exist.")
        exit(EXIT_FAILURE)
    }
}




