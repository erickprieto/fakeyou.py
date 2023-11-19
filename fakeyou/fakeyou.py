import requests
import json
import logging
import re
from uuid import uuid4
from .objects import *
from .exception import *


class FakeYou():
	
    """ A class to interact with FakeYou API for various operations like login, 
    voice listing, text-to-speech conversion, and more. """

    def __init__(self, verbose: bool = False):
        """ Initializes the FakeYou instance. """
        self.baseurl = "https://api.fakeyou.com/"
        self.headers = {
            "accept": "application/json",
            "content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers = self.headers
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        logging.debug("Session created")
	
    def _handle_response(self, response, success_codes=[200], fail_exceptions={}):
        """ Generic handler for API responses. """
        if response.status_code in success_codes:
            return response.json()
        else:
            exception = fail_exceptions.get(response.status_code, RequestError)
            raise exception()

    def login(self, username, password):
        """ Logs in to the FakeYou API and returns the session information. """
        login_payload = {"username_or_email": username, "password": password}
        logging.debug("Sending Login request")
        response = self.session.post(self.baseurl + "login", json=login_payload)
        logging.debug("Login request sent")
        fail_exceptions = {401: InvalidCredentials, 429: TooManyRequests}
        return self._handle_response(response, fail_exceptions=fail_exceptions)

    def list_voices(self):
        """
        Retrieves a list of available voices.
        """
        response = self._get_request("tts/voices")
        return response.get('voices', [])

    def list_voice_categories(self):
        """
        Retrieves a list of voice categories.
        """
        response = self._get_request("tts/categories")
        return response.get('categories', [])

    def get_voices_by_category(self, category_token):
        """
        Retrieves voices available in a specific category.
        """
        response = self._get_request(f"tts/voices/{category_token}")
        return response.get('voices', [])

    def _get_request(self, endpoint):
        """
        Performs a GET request to the specified API endpoint and handles responses.
        """
        response = self.session.get(url=self.baseurl + endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise RequestError(f"Failed to fetch data from {endpoint}: {response.text}")

	
    def make_tts_job(self, text: str, ttsModelToken: str):
        """ Creates a text-to-speech job and returns its token. """
        payload = {
            "uuid_idempotency_token": str(uuid4()),
            "tts_model_token": ttsModelToken,
            "inference_text": text
        }
        response = self.session.post(
            url=self.baseurl + "tts/inference", 
            data=json.dumps(payload)
        )
        fail_exceptions = {400: RequestError, 429: TooManyRequests}
        return self._handle_response(response, fail_exceptions=fail_exceptions)
	
    def tts_poll(self, poll_id):
        """
        Polls the status of a text-to-speech request.

        Args:
            poll_id (str): The ID of the TTS request to poll.

        Returns:
            dict: A dictionary containing the status and result of the TTS request.

        Raises:
            RequestError: If the request to the API fails.
        """
        endpoint = f"tts/poll/{poll_id}"
        response = self._get_request(endpoint)

        if 'status' in response:
            return response
        else:
            raise RequestError(f"Invalid response received for poll ID {poll_id}")

    def say(self, voice, text):
        """
        Converts text to speech using a specified voice.

        Args:
            voice (str): The token of the voice to use.
            text (str): The text to convert to speech.

        Returns:
            dict: A dictionary containing the poll ID for the TTS request.

        Raises:
            RequestError: If the TTS request fails.
        """
        data = {"voice": voice, "text": text}
        response = self.session.post(url=self.baseurl + "tts/say", json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise RequestError(f"TTS request failed: {response.text}")
	
    def tts_status(self, poll_id):
        """
        Retrieves the status of a text-to-speech conversion process.

        This method polls the current status of a TTS request using its unique ID,
        returning information about whether the TTS conversion is complete,
        and if completed, the URL to download the generated audio.

        Args:
            poll_id (str): The unique ID of the TTS request.

        Returns:
            dict: A dictionary with two keys: 'completed' (bool) indicating if the TTS 
                  conversion is finished, and 'download_url' (str or None) containing 
                  the URL to download the audio if conversion is complete.

        Raises:
            RequestError: If the polling request fails or returns an unexpected response.
        """
        poll_response = self.tts_poll(poll_id)

        if poll_response['status'] == 'done':
            return {
                'completed': True,
                'download_url': poll_response.get('download_url')
            }
        elif poll_response['status'] in ['in_progress', 'pending']:
            return {'completed': False, 'download_url': None}
        else:
            raise RequestError(f"Unexpected status received: {poll_response['status']}")


    def get_tts_leaderboard(self):
        """
        Retrieves the current leaderboard for text-to-speech (TTS) conversions.

        This method provides a list of the top TTS conversions based on popularity
        and user ratings. It is useful for understanding trending or highly rated
        TTS conversions within the FakeYou community.

        Returns:
            list: A list of dictionaries, each representing a TTS conversion on the
                  leaderboard, with relevant details such as conversion ID, user rating,
                  and other metadata.
        """
        response = self.session.get(f'{self.api_url}/tts/leaderboard')
        self._check_response(response)
        return response.json()
	
    def get_w2l_leaderboard(self):
        """
        Retrieves the current leaderboard for wake word to lip-sync (W2L) conversions.

        This method returns a list of the most popular or highly rated W2L conversions,
        showcasing top conversions in the FakeYou community for wake word synchronization
        with lip movement in videos.

        Returns:
            list: A list of dictionaries, each representing a W2L conversion on the
                  leaderboard, with details like conversion ID, user rating, and other
                  metadata.
        """
        response = self.session.get(f'{self.api_url}/w2l/leaderboard')
        self._check_response(response)
        return response.json()

	
    def get_last_events(self):
        """
        Retrieves the most recent events in the FakeYou platform.

        This method provides information about the latest activities or updates,
        such as new TTS or W2L conversions, user achievements, or community
        announcements.

        Returns:
            list: A list of dictionaries, each containing details about a recent
                  event, including type, description, and relevant metadata.
        """
        response = self.session.get(f'{self.api_url}/events/last')
        self._check_response(response)
        return response.json()

    def get_user(self, user_id):
        """
        Retrieves details of a specific user by their ID.

        This method provides detailed information about a user on the FakeYou
        platform, including their profile, contributions, and activity.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            dict: A dictionary containing detailed information about the user,
                  including username, profile picture, and activity history.
        """
        response = self.session.get(f'{self.api_url}/users/{user_id}')
        self._check_response(response)
        return response.json()

	
    def get_queue(self):
        """
        Retrieves the current status of the TTS and W2L processing queues.

        This method provides insights into the workload and pending tasks
        in the FakeYou conversion queues, useful for estimating wait times
        and overall system load.

        Returns:
            dict: A dictionary with details about the current queue status,
                  including number of pending conversions and average wait time.
        """
        response = self.session.get(f'{self.api_url}/queue')
        self._check_response(response)
        return response.json()
			
    def create_account(self, username, password, email):
        """
        Creates a new user account on the FakeYou platform.

        This method registers a new user with a provided username, password,
        and email address. It's essential for new users to gain access to
        the FakeYou services and community.

        Args:
            username (str): The desired username for the new account.
            password (str): The password for the new account.
            email (str): The email address associated with the new account.

        Returns:
            dict: A dictionary containing information about the newly created
                  user account, including user ID and profile details.
        """
        payload = {'username': username, 'password': password, 'email': email}
        response = self.session.post(f'{self.api_url}/users', data=payload)
        self._check_response(response)
        return response.json()

	
    def make_w2l_job(self, file, template_token):
        """
        Creates a W2L (Wave2Lip) job using a file and a template token.
        """
        file_name = file.name
        name = file_name.split("/")[-1] if "/" in file_name else file_name

        files = {'file': (name, file, 'multipart/form-data')}
        data = {'template_token': template_token}

        response = self.session.post(url=self.baseurl + "w2l/inference", files=files, data=data)
        if response.status_code == 200:
            return response.json()["inference_job_token"]
        else:
            raise RequestError(f"Failed to create W2L job: {response.text}")

    def w2l_poll(self, ijt):
        """
        Polls the status of a W2L job until completion or failure.
        """
        while True:
            response = self.session.get(url=self.baseurl + f"w2l/job/{ijt}")
            if response.status_code == 200:
                job_status = response.json()["state"]["status"]
                if job_status in ["started", "pending"]:
                    time.sleep(5)
                    continue
                elif job_status == "complete_success":
                    return response.json()
                else:
                    raise RequestError(f"W2L job failed with status: {job_status}")
            else:
                raise RequestError(f"Failed to poll W2L job: {response.text}")

    def lip_sync(self, file, template_token):
        """
        Performs the lip-sync operation using a file and a template token.
        """
        ijt = self.make_w2l_job(file, template_token)
        return self.w2l_poll(ijt)

    def w2l(self, audio_id, video_id):
        """
        Initiates a wake word to lip-sync (W2L) conversion process.

        This method combines a selected audio ID with a video ID to create a
        synchronized lip movement in the video according to the audio.

        Args:
            audio_id (str): The ID of the audio file to be used in the conversion.
            video_id (str): The ID of the video file where the lip-sync will be applied.

        Returns:
            dict: A dictionary containing information about the W2L conversion process,
                  including the conversion ID and status.
        """
        payload = {'audio_id': audio_id, 'video_id': video_id}
        response = self.session.post(f'{self.api_url}/w2l', data=payload)
        self._check_response(response)
        return response.json()

    def delete_tts_result(self, conversion_id):
        """
        Deletes a specific text-to-speech (TTS) conversion result.

        This method allows users to remove a TTS conversion from their account,
        typically used for managing space or clearing unwanted conversions.

        Args:
            conversion_id (str): The ID of the TTS conversion to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        response = self.session.delete(f'{self.api_url}/tts/{conversion_id}')
        self._check_response(response)
        return response.ok

	
    def delete_w2l_result(self, conversion_id):
        """
        Deletes a specific wake word to lip-sync (W2L) conversion result.

        This method is used to remove a W2L conversion from the user's account.
        It helps in managing account space and organizing conversions.

        Args:
            conversion_id (str): The ID of the W2L conversion to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        response = self.session.delete(f'{self.api_url}/w2l/{conversion_id}')
        self._check_response(response)
        return response.ok

    def logout(self):
        """
        Logs out the current user from the FakeYou platform.

        This method ends the current session and invalidates the session token,
        ensuring that the user's account is secure after they finish their activities.

        Returns:
            bool: True if the logout was successful, False otherwise.
        """
        response = self.session.post(f'{self.api_url}/logout')
        self._check_response(response)
        return response.ok

	