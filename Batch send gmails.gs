function sendEmailsWithAttachments() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();

  for (var i = 1; i < 70; i++) { // <data.length
    var email = data[i][3]; // Assuming email is in the correct column
    var firstName = (data[i][0]); // Assuming first name is in the correct column
    var documentId = (data[i][5]).split("/")[5]; // Assuming Document ID is in the correct column
    var resumeId = (data[i][6]).split("/")[5];
    var status = data[i][7];
    if (status === "Email Sent") {
      Logger.log('Skipping... ');
      continue;
    }

    Logger.log('Document ID: ' + documentId); // Check if the document ID is valid
    
    var subject = "Accounting Internship";
    //var body = "Hi " + firstName + ",\n\nDocument attached.\n\nBest regards,\nYour Name";
    var body = "I am writing to express my interest in applying for an internship opportunity within your esteemed organization. I have pursued a degree in Accounting at Kabarak University, yet to graduate in December 2024. I am excited about this opportunity to learn and grow in the field of accounting. Please find attached my application letter and resume detailing my qualifications and experiences.\n\nAs an aspiring accountant, I am eager to gain practical experience and knowledge from " + firstName + ". I look forward to hearing from you. \n\n Best Regards, \nPhemmy Chepkwony.";

    try {
      // Get the file by ID
      var file = DriveApp.getFileById(documentId);
      var resume = DriveApp.getFileById(resumeId);
      Logger.log('File retrieved: ' + file.getName());
      Logger.log('File retrieved: ' + resume.getName());
      
      // Send the email with attachment
      MailApp.sendEmail({
        to: email,
        subject: subject,
        body: body,
        attachments: [file.getAs(MimeType.PDF), resume.getAs(MimeType.PDF)] // Change MimeType if necessary
      });
      sheet.getRange(i + 1, 8).setValue("Email Sent");
      var sleepTime = Math.floor(Math.random() * (5000 - 2000 + 1)) + 2000;
      Logger.log('Email sent\nSleeping abit... ' + sleepTime + ' s');
      Utilities.sleep(sleepTime);
    } 
    catch (e) {
      Logger.log('Error retrieving file: ' + e.message);
      // Skip to the next iteration if there's an error
      continue;
    }
  }
}
