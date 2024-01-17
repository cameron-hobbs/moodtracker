class PatientArchiver:

    def __init__(self, patient):
        self._patient = patient

    def archive(self):
        self._patient.hidden = True
        self._patient.receive_mood_tracker_sms = False
        self._patient.save()

    def dearchive(self):
        self._patient.hidden = False
        self._patient.save()
