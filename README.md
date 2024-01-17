A simple "mood tracker" backend.

Uses JWT for authentication. Users are doctors.

Users can then add patients and edit their details at any time.

A patient can then be selected and treatment added for them.

Every day at midday an SMS text is sent out to every patient asking
them to rate their mood from 1-10. The patient then replies to that 
text and their mood is tracked in the database.

SMS Provider was TextLocal, we were using virtual LONG phone numbers.

On the frontend the doctor could basically see graphs and other statistics
for how treatment is effecting their patients mood.

This was originally built for a ketamine clinic (studying effect of ketamine on mental health)
but never materialized and I owned the IP for the code and servers. It was 
fully deployed and ready, with all unit tests passing and been tested live for a short while.
