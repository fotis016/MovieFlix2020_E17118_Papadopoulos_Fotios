---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ΣΗΜΕΙΩΣΗ ΠΡΟΣ ΤΟΥΣ ΕΞΕΤΑΣΤΕΣ ΤΗΣ ΕΡΓΑΣΙΑΣ:
Στην εργασία, έχουν γίνει οι εξής διαφοροποιήσεις σχετικά με ότι αναγράφεται στην εκφώνηση:
Το πεδίο "Actors" είναι string, όχι πίνακας.
Η διαγραφή ταινίας δεν θα αναζητεί να διαγράψει την παλαιότερη ταινία με βάση το keyword. Κάθε ταινία που εισάγεται στην βάση δεδομένων θα πρέπει να έχει ξεχωριστό τίτλο, επομένως
για την διαγραφή της θα πρέπει να εισαχθεί ο τίτλος της ταινίας ακριβώς όπως έχει αποθηκευτεί στην βάση δεδομένων.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


This service has been developed in order to set up and maintain a movie database, accessible through web. Users are split into 2 groups, standard users and admin users.
Standard and admin users have access to these options: 

1. Search for a movie stored in database
2. Print all info for all movies stored in database
3. Print all comments from all users for a specific movie
4. Rate a movie
5. Remove rating
6. Insert a comment for a movie
7. Print every comment a user has left
8. Print every rating a user has left
9. Delete a specific comment
10. Terminate account

Only admin users have access to these options:

11. Insert new movie in database
12. Delete a movie from database
13. Update information of a specific movie
14. Delete a specific comment a different user has left for a movie
15. Upgrade a standard user to admin
16. Terminate a standard user's account

HOW TO LAUNCH THE SERVICE - INSTRUCTIONS:
Navigate to the folder contents, then access the flask folder. You can then run the service by executing this command: "sudo docker-compose up --build"
which essentially launches both the web service and the mongodb through the "docker-compose.yml" file. In order to login and manage the web service, open up the browser and
type in the url tab: localhost:27017
You'll be prompted to either login or register your account. In case you are running the service for the very first time, a default admin account will be created with the specific
credentials: email: admin@mail.com, password: 1111
