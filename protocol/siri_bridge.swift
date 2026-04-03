import Foundation
import AVFoundation

/**
 * SiriBridge - The "Summoning Voice" for Phantasm Avatars.
 * Bridges the Bioglobe narrative to macOS Speech Synthesis.
 */

class SiriBridge {
    private let synthesizer = AVSpeechSynthesizer()
    
    func speak(persona: String, dialogue: String, resonate: Bool = true) {
        print("🔊 [SIRI BRIDGE] \(persona) is speaking...")
        
        let processedDialogue = resonate ? applyResonanceCalibrator(dialogue) : dialogue
        let utterance = AVSpeechUtterance(string: processedDialogue)
        
        // Select an 'Experienced' Siri voice identifier
        // Preferred: com.apple.voice.compact.en-GB.Daniel or American Siri
        if let siriVoice = AVSpeechSynthesisVoice(identifier: "com.apple.ttsbundle.siri_female_en-US_compact") ?? 
                          AVSpeechSynthesisVoice(identifier: "com.apple.voice.compact.en-GB.Daniel") {
            utterance.voice = siriVoice
        }
        
        utterance.rate = 0.48 
        utterance.pitchMultiplier = 0.88
        utterance.volume = 1.0
        utterance.preUtteranceDelay = 0.2
        
        synthesizer.speak(utterance)
    }
    
    private func applyResonanceCalibrator(_ input: String) -> String {
        print("📡 [RESONANCE] Calibrating Hz band for optimal Phantasm delivery...")
        // In this layer, we simulate frequency shifting by adding subtle timing pauses
        // which the synthesizer interprets as natural breath/cadence.
        return input.replacingOccurrences(of: ".", with: "...").replacingOccurrences(of: ",", with: ", ...")
    }
}

// Command line entry point for Phantasm speech
let args = CommandLine.arguments
if args.count >= 3 {
    let persona = args[1]
    let dialogue = args[2]
    let bridge = SiriBridge()
    bridge.speak(persona: persona, dialogue: dialogue)
    
    // Wait for speech to finish (for CLI demonstration)
    while bridge.synthesizer.isSpeaking {
        RunLoop.current.run(mode: .default, before: Date(timeIntervalSinceNow: 0.1))
    }
}
