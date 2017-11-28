import PackageDescription

let package = Package(
    name: "Partay",
    targets: [],
    dependencies: [
        .Package(url: "https://github.com/IBM-Swift/BlueSocket.git",
                 majorVersion: 0),
    ]
)
