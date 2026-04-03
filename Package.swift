// swift-tools-version: 5.10
import PackageDescription

let package = Package(
    name: "HardwareOptimizationSystem",
    platforms: [
        .macOS(.v14)
    ],
    products: [
        .library(
            name: "HardwareOptimization",
            targets: ["HardwareOptimization"]
        ),
        .executable(
            name: "HardwareOptimizationDaemon",
            targets: ["HardwareOptimizationDaemon"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-system", from: "1.4.0"),
        .package(url: "https://github.com/apple/swift-log", from: "1.6.0")
    ],
    targets: [
        .target(
            name: "HardwareOptimization",
            dependencies: [
                .product(name: "SystemPackage", package: "swift-system"),
                .product(name: "Logging", package: "swift-log")
            ],
            path: "Sources",
            sources: [
                "Algorithm/AlgorithmEngine.swift",
                "Algorithm/OptimalThresholdOptimizer.swift",
                "Hardware/HardwareManager.swift",
                "Protocol/XPCProtocol.swift"
            ],
            swiftSettings: [
                .unsafeFlags(["-target", "x86_64-apple-macosx14.0"])
            ]
        ),
        .executableTarget(
            name: "HardwareOptimizationDaemon",
            dependencies: [
                "HardwareOptimization",
                .product(name: "Logging", package: "swift-log")
            ],
            path: "Sources/Daemon",
            swiftSettings: [
                .unsafeFlags(["-target", "x86_64-apple-macosx14.0"])
            ]
        )
    ]
)
