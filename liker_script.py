import os
import time
import logging
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException
)

# Créer le répertoire logs s'il n'existe pas
os.makedirs('/app/logs', exist_ok=True)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/app/logs/linkedin_bot.log")
    ]
)

def decrypt_file(encrypted_file):
    try:
        with open("encryption.key", "rb") as key_file:
            key = key_file.read()
        cipher = Fernet(key)
        with open(encrypted_file, "rb") as file:
            encrypted_data = file.read()
        return cipher.decrypt(encrypted_data).decode()
    except Exception as e:
        logging.error(f"Erreur lors du déchiffrement : {e}")
        raise

def login_to_linkedin(driver, username, password):
    try:
        logging.info("Tentative de connexion à LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "feed-identity-module"))
        )
        logging.info("Connexion réussie à LinkedIn.")
    except Exception as e:
        logging.error(f"Erreur lors de la connexion : {e}")
        raise

def check_logged_in(driver):
    try:
        # Vérifie si l'utilisateur est toujours connecté
        driver.find_element(By.CLASS_NAME, "feed-identity-module")
        return True
    except NoSuchElementException:
        logging.warning("Session expirée ou utilisateur déconnecté.")
        return False

def like_latest_posts(driver, profile_url):
    """
    Accède à la page des activités récentes d'un profil LinkedIn,
    trie les posts par ordre décroissant d'heure, et like les deux plus récents.
    """
    try:
        # Construire l'URL pour "Activité récente"
        recent_activity_url = profile_url.rstrip('/') + "/recent-activity/all/"
        logging.info(f"Visite de la page des activités récentes : {recent_activity_url}")
        driver.get(recent_activity_url)
        time.sleep(5)  # Attendre le chargement complet de la page

        # Localiser tous les posts
        posts = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@data-urn, 'urn:li:activity')]"))
        )

        if not posts:
            logging.info("Aucun post trouvé sur la page d'activités récentes.")
            return

        logging.info(f"{len(posts)} posts trouvés sur la page d'activités récentes.")

        # Récupérer les heures des posts
        posts_with_time = []
        for post in posts:
            try:
                # Récupérer l'heure de publication
                time_element = post.find_element(By.XPATH, ".//span[@aria-hidden='true'][contains(text(), 'h') or contains(text(), 'j')]")
                time_text = time_element.text.strip()
                logging.info(f"Heure du post : {time_text}")

                # Ajouter le post et son heure à la liste
                posts_with_time.append((post, time_text))
            except NoSuchElementException:
                logging.warning("Impossible de récupérer l'heure d'un post.")
                continue

        # Trier les posts par heure (ex. '4 h', '2 j', etc.)
        def parse_time(time_str):
            if "h" in time_str:  # Convertir les heures en minutes
                return int(time_str.split(" ")[0]) * 60
            elif "j" in time_str:  # Convertir les jours en minutes
                return int(time_str.split(" ")[0]) * 1440
            else:  # Autres cas (par défaut, considérer 0 pour les plus récents)
                return 0

        posts_with_time.sort(key=lambda x: parse_time(x[1]))

        # Prendre les deux posts les plus récents
        most_recent_posts = posts_with_time[:2]

        for i, (post, time_text) in enumerate(most_recent_posts, start=1):
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", post)
                time.sleep(1)

                # Localiser le bouton "J’aime"
                like_button = WebDriverWait(post, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        ".//button[contains(@class, 'react-button__trigger') and contains(@aria-label, 'J’aime')]"
                    ))
                )

                # Vérifiez l'état du bouton
                if like_button.get_attribute("aria-pressed") == "true":
                    logging.info(f"Post #{i} : déjà liké (publié il y a {time_text}).")
                else:
                    like_button.click()
                    logging.info(f"Post #{i} : liké avec succès (publié il y a {time_text}).")
                    time.sleep(2)
            except Exception as e:
                logging.error(f"Erreur inattendue sur le post #{i} (publié il y a {time_text}) : {e}")
    except Exception as e:
        logging.error(f"Erreur lors du traitement du profil {profile_url} : {e}")



def main_loop(driver, username, password, profiles, check_interval=60):
    """
    Boucle principale : vérifie et like les 2 posts les plus récents pour chaque profil.
    """
    try:
        login_to_linkedin(driver, username, password)
        while True:
            if not check_logged_in(driver):
                logging.error("Session expirée. Arrêt du script.")
                break

            logging.info("=== Début du cycle de vérification ===")
            for profile_url in profiles:
                try:
                    like_latest_posts(driver, profile_url)
                except TimeoutException:
                    logging.error(f"Timeout lors du traitement du profil {profile_url}.")
                except Exception as e:
                    logging.error(f"Erreur critique lors du traitement du profil {profile_url} : {e}")


            logging.info(f"=== Fin du cycle. Pause de {check_interval} secondes ===")
            time.sleep(check_interval)
    except KeyboardInterrupt:
        logging.info("Arrêt par l'utilisateur (CTRL+C)")
    except Exception as e:
        logging.critical(f"Erreur critique dans la boucle principale : {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            logging.info("Driver fermé proprement")

def setup_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    return chrome_options

if __name__ == "__main__":
    try:
        linkedin_username = decrypt_file("/run/secrets/linkedin_username.enc")
        linkedin_password = decrypt_file("/run/secrets/linkedin_password.enc")
        target_profiles = decrypt_file("/run/secrets/linkedin_profiles.enc").splitlines()

        chrome_options = setup_chrome_options()
        service = Service("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        main_loop(driver, linkedin_username, linkedin_password, target_profiles)
    except Exception as e:
        logging.critical(f"Erreur critique du programme : {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            logging.info("Driver fermé proprement")
