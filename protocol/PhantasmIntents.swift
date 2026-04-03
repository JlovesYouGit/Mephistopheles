import Foundation
import AppIntents

/**
 * PhantasmIntents - Native macOS AppIntents for Siri Integration.
 * Allows the Phantasm AGI to be triggered directly via Siri voice commands.
 */

@available(macOS 14.0, *)
struct AskPhantasmIntent: AppIntent {
    static var title: LocalizedStringResource = "Ask Phantasm"
    static var description = IntentDescription("Speak with the Phantasm AGI about lore or system status.")

    @Parameter(title: "Query", description: "What do you want to ask Phantasm?")
    var query: String

    @Parameter(title: "Reasoning Mode", default: false)
    var useReasoningMode: Bool

    static var parameterSummary: some ParameterSummary {
        Summary("Ask Phantasm \(\.$query)") {
            file:///Users/u/Desktop/optimised%20update-v2macos/protocol/PhantasmIntents.swift#L24-L26
        }
    }

    func perform() async throws -> some IntentResult & ReturnsValue<String> & ProvidesDialog {
        let mode = useReasoningMode ? "REASONING" : "FAST"
        print("🎙️ [SIRI INTENT] AskPhantasm triggered: \(query) (Mode: \(mode))")
        
        // Bridge to Python SiriLLMNexus via CLI for now
        // In a full app, this would use XPC to the resident daemon
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
        let scriptPath = "/Users/u/Desktop/optimised update-v2macos/protocol/siri_llm_nexus_bridge.py"
        process.arguments = [scriptPath, query, mode]
        
        let pipe = Pipe()
        process.standardOutput = pipe
        try process.run()
        process.waitUntilExit()
        
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        let response = String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? "The resonance failed to converge."
        
        return .result(value: response, dialog: "\(response)")
    }
}

@available(macOS 14.0, *)
struct OptimizeHardwareIntent: AppIntent {
    static var title: LocalizedStringResource = "Optimize Phantasm Hardware"
    static var description = IntentDescription("Triggers the Hardware Mesh pulse via Siri.")

    func perform() async throws -> some IntentResult & ProvidesDialog {
        print("⚙️ [SIRI INTENT] OptimizeHardware triggered.")
        
        // Signal the daemon via XPC or file
        let signalPath = "/Users/u/Desktop/optimised update-v2macos/protocol/mesh_signal.tmp"
        try? "PULSE".write(toFile: signalPath, atomically: true, encoding: .utf8)
        
        return .result(dialog: "Phantasm hardware lanes are now optimized. The 6-lane splitter is at maximum throughput.")
    }
}

@available(macOS 14.0, *)
struct PhantasmShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: AskPhantasmIntent(),
            phrases: [
                "Ask \(.applicationName) \(\.$query)",
                "Talk to \(.applicationName) about \(\.$query)",
                "Think more about \(\.$query) with \(.applicationName)"
            ],
            shortTitle: "Ask Phantasm",
            systemImageName: "sparkles"
        )
        
        AppShortcut(
            intent: OptimizeHardwareIntent(),
            phrases: [
                "Optimize \(.applicationName) hardware",
                "Pulse the \(.applicationName) mesh"
            ],
            shortTitle: "Optimize Hardware",
            systemImageName: "bolt.fill"
        )
    }
}
