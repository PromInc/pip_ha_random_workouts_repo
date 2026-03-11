# PIP HA Random Workouts 🏋️‍♂️

A custom Home Assistant integration that pulls workout collections from remote JSON files and selects a random routine for you. Designed for both hands-free automation and interactive dashboard use.

## Features
- **Automation Ready:** Trigger a random workout via service call and cast it directly to a Smart TV.
- **Dashboard Support:** Track the current workout title and video via a dedicated sensor.
- **Custom Collections:** Input multiple JSON URLs to pool different types of workouts.

## Installation

### Via HACS (Recommended)
1. Open **HACS** in Home Assistant.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Paste the URL of this GitHub repository.
4. Select **Integration** as the category and click **Add**.
5. Find "PIP Random Workouts" and click **Download**.
6. Restart Home Assistant.

### Manual
1. Copy the `custom_components/pip_ha_random_workouts` folder into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.

## Configuration
1. Go to **Settings > Devices & Services**.
2. Click **Add Integration** and search for **PIP Random Workouts**.
3. Enter your list of JSON URLs (separated by commas).
   - *Example:* `https://example.com/list1.json, https://example.com/list2.json`

## Usage

### 1. Automation Path (Smart TV)
To automatically play a workout on your TV (e.g., at 7:00 AM), use the following service call in your automation:

```yaml
service: pip_ha_random_workouts.pick_random
data:
  entity_id: media_player.living_room_tv
```

## Changelog

### 1.0.5
- debug

### 1.0.4
- debug

### 1.0.3
- version bump

### 1.0.2
- hacs structure update

### 1.0.1
- Improve how enties are loaded

### 1.0.0
- Initial release
