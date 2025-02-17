import requests

# def __init__(self, base_url, settings=None):
# def new_notepad(self, settings=None):
# def delete_notepad(self):
# def set_notepad(self):
# def set_notepad_text(self, text):
# def get_notepad_text(self):
# def notepad_generate(self):
# def rename_notepad(self, new_name):
# def list_notepads(self):

class Notepad:
    def __init__(self, base_url, settings=None, debug=False):
        self.base_url = base_url
        self.debug = debug
        self.headers = {'Content-Type': 'application/json'}
        self.notepad_uuid = None
        self.text = None
        self.new_notepad(settings)

    def new_notepad(self, settings=None):
        data = {"text": "", "new_name": "Delete"}
        if settings is not None:
            data['settings'] = settings
        response = requests.post(f"{self.base_url}/api/new_notepad", headers=self.headers, json=data)

        if response.status_code == 200:
            self.notepad_uuid = response.json()['notepad']['notepad_uuid']
            self.print(f"Created new notepad: {self.notepad_uuid}")
        else:
            self.print(f"Error creating notepad: {response.text}")

    def delete_notepad(self):
        data = {'notepad_uuid': self.notepad_uuid}
        response = requests.post(f"{self.base_url}/api/delete_notepad", headers=self.headers, json=data)
        if response.status_code == 200:
            self.print(f"Deleted notepad: {self.notepad_uuid}")
        else:
            self.print(f"Error deleting notepad: {response.text}")

    # Set the current notepad to the given notepad
    def set_notepad(self):
        data = {'notepad_uuid': self.notepad_uuid}
        response = requests.post(f"{self.base_url}/api/set_notepad", headers=self.headers, json=data)
        if response.status_code == 200:
            self.print(f"Set active notepad: {self.notepad_uuid}")
        else:
            self.print(f"Error setting active notepad: {response.text}")

    def set_notepad_text(self, text):
        data = {'text': text}
        response = requests.post(f"{self.base_url}/api/set_notepad_text", headers=self.headers, json=data)
        if response.status_code == 200:
            self.print(f"Set notepad text")
        else:
            self.print(f"Error setting notepad text: {response.text}")

    # Returns current notepad text 
    # Set the current notepad to be the given notepad
    def get_notepad_text(self):
        text = ""
        data = {"notepad_uuid": self.notepad_uuid}
        response = requests.post(f"{self.base_url}/api/set_notepad", json=data)
        if response.status_code == 200:
            text = response.json()['notepad']['text']
        else:
            self.print(f"Error getting notepad text: {response.text}")
        return text

    def notepad_generate(self):
        data = {
            "context": self.get_notepad_text(),
            "context_post": ""
        }
        response = requests.post(f"{self.base_url}/api/notepad_generate", headers=self.headers, json=data)
        if response.status_code == 200:
            self.print(f"Generated notepad text")
        else:
            self.print(f"Error generating notepad text: {response.text}")

    def rename_notepad(self, new_name):
        data = {'new_name': new_name}
        response = requests.post(f"{self.base_url}/api/rename_notepad", headers=self.headers, json=data)
        if response.status_code == 200:
            self.print(f"Renamed notepad to: {new_name}")
        else:
            self.print(f"Error renaming notepad: {response.text}")

    def list_notepads(self):
        """Retrieve the list of notepads and the current notepad."""
        response = requests.get(f"{self.base_url}/api/list_notepads", headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            notepads = result.get('notepads', [])
            current_notepad = result.get('current_notepad', None)
            self.print(f"List of notepads: {notepads}")
            self.print(f"Current notepad: {current_notepad}")
            return notepads
        else:
            self.print(f"Error retrieving notepads: {response.text}")

    def print(self, message):
        if self.debug:
            print(message)
# Deprecated Functions
# def update_notepad_settings(self, settings):
# def cancel_notepad_generate(self):

    # def update_notepad_settings(self, settings):
    #     data = {'settings': settings}
    #     response = requests.post(f"{self.base_url}/api/update_notepad_settings", headers=self.headers, json=data)
    #     if response.status_code == 200:
    #         print(f"Updated notepad settings.")
    #     else:
    #         print(f"Error updating notepad settings: {response.text}")

    # def cancel_notepad_generate(self):
    #     response = requests.post(f"{self.base_url}/api/cancel_notepad_generate", headers=self.headers)
    #     if response.status_code == 200:
    #         print(f"Notepad generation canceled.")
    #     else:
    #         print(f"Error canceling notepad generation: {response.text}")














