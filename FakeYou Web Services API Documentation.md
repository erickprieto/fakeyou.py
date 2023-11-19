# FakeYou Web Services API Documentation

## Authentication Endpoints

### `/api/auth/login`
- **Description:** Endpoint for user login.

### `/api/auth/logout`
- **Description:** Endpoint for user logout.

## Text-to-Speech (TTS) Endpoints

### `/api/tts/create`
- **Description:** Endpoint to create a new TTS job.

### `/api/tts/poll/:job_id`
- **Description:** Endpoint to check the status of a TTS job.

### `/api/tts/status`
- **Description:** Endpoint to get the status of the TTS service.

### `/api/tts/delete/:result_id`
- **Description:** Endpoint to delete a TTS result.

### `/api/tts/leaderboard`
- **Description:** Endpoint to get the TTS usage leaderboard.

## Wake Word to Lip-sync (W2L) Endpoints

### `/api/w2l/create`
- **Description:** Endpoint to create a new W2L job.

### `/api/w2l/delete/:result_id`
- **Description:** Endpoint to delete a W2L result.

### `/api/w2l/leaderboard`
- **Description:** Endpoint to get the W2L usage leaderboard.

## User Management Endpoints

### `/api/user/create`
- **Description:** Endpoint for creating a new user account.

### `/api/user/info`
- **Description:** Endpoint to retrieve current user's details.

### `/api/user/queue`
- **Description:** Endpoint to get the user's current job queue.

## Miscellaneous Endpoints

### `/api/events/last`
- **Description:** Endpoint to get the latest events related to the user's account.

## Voice Management Endpoints

### `/api/voices/list`
- **Description:** Endpoint to list available voices for TTS.

### `/api/voices/categories`
- **Description:** Endpoint to list voice categories.

### `/api/voices/category/:category_name`
- **Description:** Endpoint to get voices by category.