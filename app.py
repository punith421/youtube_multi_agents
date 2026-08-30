from agents.transcript_corrector import correct_transcript

def main():

    print("=" * 60)
    print("🎬 YOUTUBE MULTI AGENT")
    print("=" * 60)

    input_file = "outputs/transcript.txt"

    final_file = correct_transcript(input_file)

    print("\n✅ Done!")
    print(final_file)

if __name__ == "__main__":
    main()