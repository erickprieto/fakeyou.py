# FakeYou Python API Wrapper

## Introduction

The FakeYou Python API Wrapper is a comprehensive tool designed to interact with the FakeYou API, a platform offering various voice and video synthesis services. This wrapper simplifies tasks like text-to-speech (TTS) conversion, wake word to lip-sync (W2L) processing, and managing user accounts.

## Installation

To use the FakeYou Python API Wrapper, ensure that Python is installed on your system. You can then download this wrapper from the repository and import it into your project.
```python
from fakeyou import FakeYou
fakeYou = FakeYou("your_api_key")
tts_result = fakeYou.tts("Hello World", "voice_id")
```

## Usage

First, create an instance of the FakeYou class. Then, use the various methods provided to interact with the FakeYou API.

## Methods

### Authentication

#### login
- **Description:** Authenticates a user with the FakeYou API.
- **Parameters:** `username` (str), `password` (str)
- **Returns:** `bool`

#### logout
- **Description:** Logs out the current user from the FakeYou platform.
- **Returns:** `bool`

### Text-to-Speech (TTS)

#### tts
- **Description:** Initiates a TTS conversion process.
- **Parameters:** `text` (str), `voice_id` (str)
- **Returns:** `dict` containing TTS job details

#### tts_poll
- **Description:** Checks the status of a TTS conversion job.
- **Parameters:** `job_id` (str)
- **Returns:** `dict` with status and result information

#### tts_status
- **Description:** Retrieves the status of the TTS service.
- **Returns:** `str` indicating service status

#### delete_tts_result
- **Description:** Deletes a TTS result from the user's history.
- **Parameters:** `result_id` (str)
- **Returns:** `bool`

#### get_tts_leaderboard
- **Description:** Retrieves the TTS usage leaderboard.
- **Returns:** `list` of top users

### Wake Word to Lip-sync (W2L)

#### w2l
- **Description:** Initiates a W2L conversion process.
- **Parameters:** `file_path` (str), `model_id` (str)
- **Returns:** `dict` containing W2L job details

#### delete_w2l_result
- **Description:** Deletes a W2L result from the user's history.
- **Parameters:** `result_id` (str)
- **Returns:** `bool`

#### get_w2l_leaderboard
- **Description:** Retrieves the W2L usage leaderboard.
- **Returns:** `list` of top users

### User Management

#### create_account
- **Description:** Creates a new user account.
- **Parameters:** `username` (str), `password` (str), `email` (str)
- **Returns:** `bool`

#### get_user
- **Description:** Retrieves details of the current user.
- **Returns:** `dict` with user information

#### get_queue
- **Description:** Retrieves the user's current job queue.
- **Returns:** `list` of job details

### Misc

#### get_last_events
- **Description:** Retrieves the last events related to the user's account.
- **Returns:** `list` of event details

#### say
- **Description:** Shortcut for TTS conversion with immediate playback.
- **Parameters:** `text` (str), `voice_id` (str)
- **Returns:** `None`

### Voice Management

#### list_voices
- **Description:** Lists available voices for TTS conversion.
- **Returns:** `list` of voice details

#### list_voice_categories
- **Description:** Lists categories of available voices.
- **Returns:** `list` of category names

#### get_voices_by_category
- **Description:** Retrieves voices belonging to a specific category.
- **Parameters:** `category` (str)
- **Returns:** `list` of voices in the specified category