import os
import logging
import firebase_admin
from firebase_admin import credentials, db

import config
from models.hydration_data import HydrationData
from utils.hydration_calculator import calculate_remaining_water

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hydration_backend")

class FirebaseDataService:
    _initialized = False

    def __init__(self):
        self.initialize_firebase()

    def initialize_firebase(self):
        """
        Initializes Firebase Admin SDK if not already done.
        """
        if FirebaseDataService._initialized:
            return

        db_url = config.FIREBASE_DATABASE_URL
        if not db_url:
            logger.warning("FIREBASE_DATABASE_URL is not configured.")
            return

        service_account_path = config.FIREBASE_SERVICE_ACCOUNT_PATH
        if not service_account_path:
            logger.warning("FIREBASE_SERVICE_ACCOUNT_PATH is not configured.")
            return

        if not os.path.exists(service_account_path):
            logger.warning(f"Firebase service account file not found at: {service_account_path}")
            return

        try:
            # Initialize default app if not already initialized by firebase_admin
            if not firebase_admin._apps:
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': db_url
                })
            FirebaseDataService._initialized = True
            logger.info("Firebase Admin SDK successfully initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {e}")

    def fetch_today_raw_data(self) -> dict:
        """
        Fetches raw JSON data from path `/health/today` in Firebase RTDB.
        """
        if not FirebaseDataService._initialized:
            # Try initializing again in case credentials became available
            self.initialize_firebase()
            if not FirebaseDataService._initialized:
                raise RuntimeError(
                    f"Firebase is not initialized. Please configure FIREBASE_DATABASE_URL and "
                    f"ensure serviceAccountKey.json is placed at: {config.FIREBASE_SERVICE_ACCOUNT_PATH}"
                )

        try:
            ref = db.reference('/health/today')
            data = ref.get()
            if data is None:
                logger.info("Firebase path `/health/today` is empty.")
                return {}
            if not isinstance(data, dict):
                logger.warning(f"Firebase path `/health/today` returned non-dictionary type: {type(data)}")
                return {}
            return data
        except Exception as e:
            logger.error(f"Error fetching data from Firebase Realtime Database: {e}")
            raise RuntimeError(f"Firebase connection error: {e}")

    def fetch_today_hydration_data(self) -> HydrationData:
        """
        Fetches today's hydration metrics and parses them into a HydrationData model.
        Fills missing fields with default values.
        """
        raw_data = self.fetch_today_raw_data()

        # Parse variables with fallback defaults
        target_water = float(raw_data.get("targetWater", 0.0))
        drank_water = float(raw_data.get("drankWater", 0.0))
        remaining_water_from_firebase = float(raw_data.get("remainingWater", 0.0))

        # Calculate remaining water deterministically as requested
        calculated_remaining_water = calculate_remaining_water(target_water, drank_water)

        temperature = float(raw_data.get("temperature", 0.0))
        humidity = float(raw_data.get("humidity", 0.0))
        steps = int(raw_data.get("steps", 0))
        heart_rate = int(raw_data.get("heartRate", 0))
        weight = float(raw_data.get("weight", 0.0))
        last_sync = str(raw_data.get("lastSync", ""))
        timestamp = int(raw_data.get("timestamp", 0))

        return HydrationData(
            target_water=target_water,
            drank_water=drank_water,
            remaining_water_from_firebase=remaining_water_from_firebase,
            calculated_remaining_water=calculated_remaining_water,
            temperature=temperature,
            humidity=humidity,
            steps=steps,
            heart_rate=heart_rate,
            weight=weight,
            last_sync=last_sync,
            timestamp=timestamp
        )
