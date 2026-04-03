import AVFoundation

let voices = AVSpeechSynthesisVoice.speechVoices()
for voice in voices {
    print("\(voice.name) (\(voice.language)): \(voice.identifier)")
}
