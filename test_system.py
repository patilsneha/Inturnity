import io
import tkinter as tk
from tkinter import filedialog
import processor
import engine
import constants


def get_files_manually():
    """Opens a system file dialog to select resumes."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    print("📂 Please select your resume PDF(s) from the file dialog...")

    # Allow multiple file selection
    file_paths = filedialog.askopenfilenames(
        title="Select Resumes",
        filetypes=[("PDF files", "*.pdf")]
    )
    return file_paths


def simulate_real_upload():
    print(f"🚀 --- Initializing {constants.APP_NAME} Semantic Matching Test ---")

    # 1. Initialize the Engine (Load Internship CSV)
    df = engine.load_internships()
    engine.get_or_create_embeddings(df)

    # 2. Get files via System Dialog
    selected_files = get_files_manually()

    if not selected_files:
        print("❌ No files selected. Exiting test.")
        return

    for path in selected_files:
        print("\n" + "=" * 60)
        try:
            # 3. CONVERT TO BYTES (Simulating a Streamlit Upload object)
            with open(path, "rb") as f:
                file_bytes = io.BytesIO(f.read())
                filename = path.split("/")[-1]  # Get just the name for display

                print(f"📤 PROCESSING UPLOAD: {filename}")

                # 4. PROCESSOR PHASE
                raw_text = processor.extract_text_from_pdf(file_bytes)
                name = processor.extract_name(raw_text)
                email = processor.extract_email(raw_text)
                skills = processor.get_detected_skills(raw_text)

                print(f"👤 Candidate: {name}")
                print(f"📧 Email    : {email}")
                print(f"🛠️ Skills   : {', '.join(skills[:8])}...")

                # 5. ENGINE PHASE (Matching)
                resume_vec = processor.get_embedding(raw_text)
                matches = engine.get_recommendations(resume_vec)

                # 6. RESULTS
                if matches:
                    print(f"\n🎯 TOP {len(matches)} SEMANTIC MATCHES:")
                    for i, job in enumerate(matches, 1):
                        score = job['match_score']
                        role = job[constants.COL_ROLE]
                        company = job[constants.COL_COMPANY]
                        print(f"  {i}. [{score}% Match] {role} at {company}")
                else:
                    print("\n⚠️ No internships met the match threshold for this profile.")

        except Exception as e:
            print(f"❌ System Error processing {path}: {e}")

    print("\n" + "=" * 60)
    print("✅ Upload Simulation Complete!")


if __name__ == "__main__":
    simulate_real_upload()