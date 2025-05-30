import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import EMAIL, PASSWORD, MEET_URL, AUDIO_OUTPUT_PATH, TRANSCRIPT_OUTPUT_PATH, ASSEMBLY_API_KEY, METIS_API_KEY, SPEAKERS_EXPECTED
from recorder import record_continuous
from assembly_transcriber import assembly_stt_diarization
from openai_summarizer import chat_with_gpt

def Glogin(driver, mail_address, password):
    driver.get("https://accounts.google.com/ServiceLogin")
    wait = WebDriverWait(driver, 15)
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.send_keys(mail_address)
    driver.find_element(By.ID, "identifierNext").click()

    # Wait for password field to be present
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
        Glogin(driver, EMAIL, PASSWORD)
        join_meeting(driver, MEET_URL)

        record_thread = threading.Thread(target=record_continuous, args=(AUDIO_OUTPUT_PATH, stop_recording_event))
        record_thread.start()

        print("Recording... Press Ctrl+C to stop or wait for 30 minutes.")
        start_time = time.time()
        while time.time() - start_time < 1800:  # 30 minutes
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping meeting and recording...")
    finally:
        stop_recording_event.set()
        if record_thread is not None:
            record_thread.join()
        driver.quit()

        print("Transcribing with AssemblyAI...")
        diarized_text = assembly_stt_diarization(ASSEMBLY_API_KEY, SPEAKERS_EXPECTED, AUDIO_OUTPUT_PATH, TRANSCRIPT_OUTPUT_PATH)

        print("Summarizing with OpenAI...")
        summary = chat_with_gpt(diarized_text, METIS_API_KEY)

        summary_path = "output/summary.txt"
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
