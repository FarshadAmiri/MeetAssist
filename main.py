import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import *
from recorder import record_continuous
from assembly_transcriber import assembly_stt_diarization
from openai_summarizer import mom_summarizer, session_top_subjects, MOMWriterBot
from rag import upload_to_rag, retrieve_relevant_chunks


def Glogin(driver, mail_address, password):
    driver.get("https://accounts.google.com/ServiceLogin")
    wait = WebDriverWait(driver, 15)
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.send_keys(mail_address)
    driver.find_element(By.ID, "identifierNext").click()

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
    password_input.send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    time.sleep(5)


def join_meeting(driver, meeting_link):
    driver.get(meeting_link)
    time.sleep(10)
    try:
        driver.find_element(By.XPATH, "//div[@aria-label='Turn off microphone']").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//div[@aria-label='Turn off camera']").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//span[text()='Join now']").click()
    except:
        try:
            driver.find_element(By.XPATH, "//span[text()='Ask to join']").click()
        except:
            pass


def wait_until_meeting_ends(driver, check_interval=10):
    print("Waiting for the meeting to end...")
    try:
        while True:
            page_source = driver.page_source
            if "You’ve left the meeting" in page_source or "has ended" in page_source:
                print("Meeting ended.")
                break
            time.sleep(check_interval)
    except Exception as e:
        print(f"Error while checking meeting status: {e}")


def safe_action(action_fn, retries=3, wait_sec=5):
    for attempt in range(retries):
        try:
            action_fn()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(wait_sec)
    return False


def setup_driver():
    opt = Options()
    opt.add_argument("--disable-blink-features=AutomationControlled")
    opt.add_argument("--start-maximized")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
    })
    return webdriver.Chrome(options=opt)


def main():
    driver = setup_driver()
    stop_recording_event = threading.Event()
    record_thread = None

    try:
        if not safe_action(lambda: Glogin(driver, EMAIL, PASSWORD)):
            raise Exception("Login failed")

        if not safe_action(lambda: join_meeting(driver, MEET_URL)):
            raise Exception("Join meeting failed")

        # Start recording
        print(f"Recording for {RECORD_DURATION_MINUTES} minutes...")
        record_thread = threading.Thread(target=record_continuous, args=(AUDIO_OUTPUT_PATH, stop_recording_event))
        record_thread.start()

        # Wait for the configured duration
        time.sleep(RECORD_DURATION_MINUTES * 60)

    except Exception as e:
        print(f"Fatal error: {e}")

    finally:
        # Stop recording and clean up
        stop_recording_event.set()
        if record_thread:
            record_thread.join()
        driver.quit()

        print("Transcribing with AssemblyAI...")
        diarized_text = assembly_stt_diarization(
            ASSEMBLY_API_KEY,
            SPEAKERS_EXPECTED,
            AUDIO_OUTPUT_PATH,
            TRANSCRIPT_OUTPUT_PATH
        )
        
        print("Summarizing with OpenAI Metis Bot...")
        response = MOMWriterBot(METIS_API_KEY, MOMWriterBot_ID, diarized_text)
        summary = response["messages"][0]["content"]  # Extract summary text

        summary_path = "output/summary.txt"
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"Summary saved to: {summary_path}")

        print("Uploading summary to RAG vector database...")
        try:
            rag_result = upload_to_rag(METIS_API_KEY, CORPUS_ID, summary)
            print("Successfully uploaded to RAG:", rag_result)
        except Exception as e:
            print("Error uploading to RAG:", e)


if __name__ == "__main__":
    main()
