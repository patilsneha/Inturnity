import processor
import constants

# --- LIST OF TEST FILES ---
TEST_FILES = ["test1_resume.pdf", "test2_resume.pdf", "test3_resume.pdf", "test4_resume.pdf"]


def run_bulk_test():
    print(f"🚀 --- Starting Bulk Test for {constants.APP_NAME} ---")

    for filename in TEST_FILES:
        print("\n" + "=" * 50)
        print(f"📄 TESTING FILE: {filename}")
        print("=" * 50)

        try:
            # Open file in read-binary mode
            with open(filename, "rb") as file:
                # 1. Extract Text
                raw_text = processor.extract_text_from_pdf(file)

                # 2. Metadata Extraction
                name = processor.extract_name(raw_text)
                email = processor.extract_email(raw_text)
                print(f"👤 Name  : {name}")
                print(f"📧 Email : {email}")

                # 3. Skill Extraction
                skills = processor.get_detected_skills(raw_text)
                print(f"🛠️ Skills: {', '.join(skills) if skills else 'No skills detected'}")

                # 4. AI Embedding Check
                vector = processor.get_embedding(raw_text)
                if vector is not None:
                    print(f"✅ AI Vectorization Successful (Shape: {vector.shape})")

        except FileNotFoundError:
            print(f"⚠️ Warning: Could not find '{filename}'. Skipping...")
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    print("\n" + "=" * 50)
    print("✅ Bulk Testing Complete!")


if __name__ == "__main__":
    run_bulk_test()